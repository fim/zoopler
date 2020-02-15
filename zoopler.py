#!/usr/bin/env python3
import collections
import datetime
import json
import hashlib
import logging
import math
import os
import string
import re
import shutil
import sys

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from io import BytesIO

import click
import demjson
import requests
import tabulate
import tesserocr
from bs4 import BeautifulSoup as bs
from PIL import Image


CACHEDIR = ".zoopler"
DEFAULT_PAGE_SIZE = 100
ZOOPLA_BASE_URL = "https://zoopla.co.uk"
ZOOPLA_BASE_SALE_SEARCH = f"{ZOOPLA_BASE_URL}/search"

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FauxCache:
    """
    Quick way to avoid hitting zoopla and doing expensive ocr by building an
    ondisk cache for items. Ugly but hey, it works
    """

    def __init__(self, cachedir=CACHEDIR, identifier=None):
        self.cachedir = cachedir
        self.identifier = identifier

    def _get_id(self, key):
        def get_hash(key):
            return hashlib.md5(key.encode("utf-8")).hexdigest()

        cacheid = os.path.join(self.cachedir, get_hash(key))
        if self.identifier:

            return f"{cacheid}.{self.identifier}"
        return cacheid

    def get(self, key):
        try:
            cachefile = self._get_id(key)

            with open(cachefile) as f:
                content = json.loads(f.read())
            if content["ppsqm"] == content["sqm"]:
                content["ppsqm"] = content["price"] / content["sqm"]
            with open(cachefile, "w") as f:
                f.write(json.dumps(content))
                f.flush()

            with open(cachefile) as f:
                return f.read()

        except Exception as e:
            logger.debug(f"Cache miss for {key}")
            return None

    def set(self, key, value):
        try:
            cachefile = self._get_id(key)
            logger.debug(cachefile)
            logger.debug(f"Cache fill for {key}")
            with open(cachefile, "w") as f:
                f.write(str(value))
                f.flush()
        except Exception as e:
            logger.debug(e)
            return None


# cache setup
if not os.path.exists(CACHEDIR):
    os.mkdir(CACHEDIR)

SQMCache = FauxCache(identifier="sqm")
HouseCache = FauxCache(identifier="house")


def get_sqm(house):
    details_page = ZOOPLA_BASE_URL + house

    def get_hash(page):
        return hashlib.md5(details_page.encode("utf-8")).hexdigest()

    hash_name = get_hash(details_page)
    if SQMCache.get(house):
        return SQMCache.get(house)

    try:
        response = requests.get("{}#floorplan-1".format(details_page))
        m = re.compile(
            '<a href="(.*)" target="_blank" id="ui-modal-gallery-trigger-floorplan" class="ui-link">floorplan # 1</a>'
        ).search(response.text)
        if not m:
            raise Exception()
        img_response = requests.get(m.groups()[0], stream=True)
        image = Image.open(BytesIO(img_response.content))
        text = tesserocr.image_to_text(image)

        del response
        m = re.compile("([\d\.]+)\s+SQ[\.\s]*f.*", re.IGNORECASE).findall(text)
        if m:
            value_total_sqft = max(map(float, m))
            if int(value_total_sqft) < 400:
                value_total_sqft = sum(map(float, m))
            value = float(value_total_sqft * 0.092903)
            if value < 10:
                raise Exception("Something went wrong with the calculation")
            SQMCache.set(house, value)
            return float(value)
    except Exception as e:
        logger.debug(e)
        pass

    SQMCache.set(house, "NA")
    return "NA"


def parse_house_url(house):
    if HouseCache.get(house):
        return collections.defaultdict(None, json.loads(HouseCache.get(house)))
    r = requests.get(ZOOPLA_BASE_URL + house)
    html = bs(r.text, features="html5lib")
    taxonomy = html.find_all("script")[3]
    try:
        last_updated = html.find_all("span", class_="dp-price-history__item-date")[
            0
        ].string
        day, month, year = last_updated.split(" ")
        last_updated = int(
            datetime.datetime.strptime(
                f"{day.rstrip(string.ascii_lowercase)} {month} {year}", "%d %b %Y"
            ).timestamp()
        )
    except Exception as e:
        logger.debug(e)
        last_updated = 0
    m = re.match(
        ".*trackData\.taxonomy\s+=\s+(?P<info>{.*});.*",
        taxonomy.string.replace("\n", ""),
    )
    house_info = demjson.decode(m.groupdict()["info"])
    m = re.match(
        '.*trackData\.taxonomy\.url\s+=\s+"(?P<url>.*)".*',
        taxonomy.string.replace("\n", ""),
    )

    # add extra fields
    house_info.update({"url": m.groupdict()["url"]})
    house_info.update({"last_updated": last_updated})
    house_info.update({"sqm": get_sqm(house_info["url"])})
    if house_info["sqm"] and house_info["sqm"] != "NA":
        house_info.update({"ppsqm": house_info["price"] / float(house_info["sqm"])})
    else:
        house_info.update({"ppsqm": None})

    HouseCache.set(house, json.dumps(house_info))
    return collections.defaultdict(None, house_info)


@click.command()
@click.option("-m", "--min_price", default=None, type=int, help="Min price")
@click.option("-M", "--max_price", default=None, type=int, help="Max price")
@click.option("-b", "--min_beds", default=None, type=int, help="Min beds")
@click.option("-B", "--max_beds", default=None, type=int, help="Max beds")
@click.option(
    "-r",
    "--radius",
    default=None,
    type=click.Choice(["0.25", "0.5", "1", "3", "5"]),
    help="Radius in miles",
)
@click.option("-j", "--jobs", default=32, type=int, help="Max workers")
@click.option("-s", "--sort", default="last_updated", help="Sorting field")
@click.option("--json", "fjson", is_flag=True, default=False, help="Output in json")
@click.argument("location")
def search(
    location, min_price, max_price, min_beds, max_beds, radius, jobs, sort, fjson
):
    custom_params = {}
    custom_params["q"] = location
    custom_params["price_min"] = min_price
    custom_params["price_max"] = max_price
    custom_params["beds_min"] = min_beds
    custom_params["beds_max"] = max_beds
    custom_params["radius"] = radius
    custom_params["page_size"] = DEFAULT_PAGE_SIZE
    custom_params["results_sort"] = "newest_listings"
    r = requests.get(
        ZOOPLA_BASE_SALE_SEARCH, dict(custom_params, **{"section": "for-sale"})
    )
    html = bs(r.text, features="html5lib")
    houses = {
        href.get("href").split("?")[0]
        for href in html.find_all("a")
        if href.get("href") and "/details/" in href.get("href")
    }
    if not houses:
        return
    try:
        num_results = int(
            html.find("span", class_="search-refine-filters-heading-count").string
        )
    except Exception as e:
        raise click.BadParameter(f"Location '{location}' is not valid and returned no results")
    logger.info(f"Search returned {num_results} houses")
    logger.debug(
        f"Parsing {html.find_all('span', class_='listing-results-utils-count')[0].string}"
    )
    followup_url = html.find("link", {"rel": "canonical"}).get("href")
    if num_results > DEFAULT_PAGE_SIZE:
        pages_missing = int(num_results / DEFAULT_PAGE_SIZE)
        logger.debug(f"Need to parse another {pages_missing} pages")
        for page in range(2, 2 + pages_missing):
            logger.debug(f"Getting info for page {page}")
            custom_params["pn"] = page
            r = requests.get(followup_url, custom_params)
            html = bs(r.text, features="html5lib")
            logger.debug(
                f"Parsing {html.find_all('span', class_='listing-results-utils-count')[0].string}"
            )
            houses.update(
                {
                    href.get("href").split("?")[0]
                    for href in html.find_all("a")
                    if href.get("href") and "/details/" in href.get("href")
                }
            )

    logger.debug(f"parsed {len(houses)} urls")
    executor = ThreadPoolExecutor(max_workers=jobs)
    results = tuple(executor.map(parse_house_url, houses))
    if sort:
        results = sorted(
            results, key=lambda x: x[sort] if x[sort] and x[sort] != "NA" else 999999999
        )

    if not fjson:
        print(
            tabulate.tabulate(
                [
                    [
                        str(
                            (
                                datetime.datetime.now()
                                - datetime.datetime.fromtimestamp(h["last_updated"])
                            ).days
                        )
                        + "d ago"
                        if h["last_updated"]
                        else None,
                        h["price"],
                        h["outcode"],
                        h["display_address"],
                        h["tenure"],
                        f'{h["num_beds"]}/{h["num_baths"]}/{h["num_recepts"]}',
                        h["sqm"],
                        h["ppsqm"],
                        h["property_type"],
                        ZOOPLA_BASE_URL + h["url"],
                    ]
                    for h in results
                ],
                headers=[
                    "last_updated",
                    "price",
                    "postcode",
                    "address",
                    "lease",
                    "B/b/R",
                    "sqm",
                    "ppsqm",
                    "type",
                    "url",
                ],
                showindex="always",
            )
        )
    else:
        logger.debug(json.dumps(results))


if __name__ == "__main__":
    search()
