## Installation
```
$ apt-get install libleptonica-dev libtesseract-dev tesseract
$ pip install -r requirements
$ python zoopler.py --help
Usage: zoopler.py [OPTIONS] LOCATION

Options:
  -m, --min_price INTEGER        Min price
  -M, --max_price INTEGER        Max price
  -b, --min_beds INTEGER         Min beds
  -B, --max_beds INTEGER         Max beds
  -r, --radius [0.25|0.5|1|3|5]  Radius in miles
  -j, --jobs INTEGER             Max workers
  -s, --sort TEXT                Sorting field
  --json                         Output in json
  --help                         Show this message and exit.
```

## Usage

```
$ python zoopler.py -m 500000 -M 6000000 -j 32 'Camden Town Station' -s price
INFO:root:Search returned 53 houses
    last_updated      price  postcode    address                                         lease              B/b/R    sqm                   ppsqm  type         url
--  --------------  -------  ----------  ----------------------------------------------  -----------------  -------  -----------------  --------  -----------  -----------------------------------------------
 0                   500000  NW1         Billingley, Pratt Street, London NW1            leasehold          2/1/1    79.060453           6324.27  flat         https://zoopla.co.uk/for-sale/details/54032554
 1  139d ago         500000  NW1         Delancey Street, Camden Town, London NW1        leasehold          2/1/1    42.73538           11699.9   flat         https://zoopla.co.uk/for-sale/details/48216753
 2  9d ago           500000  NW1         Camden Street, Camden, London NW1                                  1/1/1    38.647648          12937.4   flat         https://zoopla.co.uk/for-sale/details/53996802
 3                   500000  NW1         Camden Street, London NW1                       share_of_freehold  1/1/1    38.833454          12875.5   flat         https://zoopla.co.uk/for-sale/details/54209370
 4  36d ago          525000  NW1         Oval Road, London NW1                                              1/1/1    48.123754          10909.4   flat         https://zoopla.co.uk/for-sale/details/53874672
 5  103d ago         525000  NW1         Leybourne Street, London NW1                                       3/1/1    85.45217939999999   6143.79  flat         https://zoopla.co.uk/for-sale/details/53206751
 6  6d ago           535000  NW1         Inverness Street, London NW1                    leasehold          1/1/1    64.10307            8345.93  flat         https://zoopla.co.uk/for-sale/details/54177046
 7  1d ago           569950  NW1         Gilbey House, 38 Jamestown Road, London NW1     share_of_freehold  1/1/1    62.059204           9183.97  flat         https://zoopla.co.uk/for-sale/details/54230721
 8  15d ago          600000  NW1         Oval Road, London NW1                                              1/1/1    NA                           flat         https://zoopla.co.uk/for-sale/details/54084753
 9  265d ago         600000  NW1         Royal College Street, London NW1                leasehold          2/1/1    70.699183           8486.66  flat         https://zoopla.co.uk/for-sale/details/51540510
10  70d ago          649000  NW1         Centric Close, Oval Road, London NW1            leasehold          1/1/     55.555994          11681.9   flat         https://zoopla.co.uk/new-homes/details/53597919
11  4d ago           660000  NW1         Castlehaven Road, Camden NW1                    leasehold          2/2/1    125.883565          5242.94  flat         https://zoopla.co.uk/for-sale/details/54197228
12                   665000  NW1         Mode, Centric Close, Oval Road, Camden NW1                         1/1/1    50.16762           13255.6   flat         https://zoopla.co.uk/new-homes/details/51770633
13  183d ago         675000  NW1         Royal College Street, London NW1                                   2/2/1    77.3510378          8726.45  flat         https://zoopla.co.uk/for-sale/details/53892164
14  126d ago         675000  NW1         Centric Close, Oval Road, London NW1            leasehold          1/1/     56.856636          11872     flat         https://zoopla.co.uk/new-homes/details/52984354
15  100d ago         678000  NW1         Centric Close, Oval Road, London NW1            leasehold          1/1/     NA                           flat         https://zoopla.co.uk/new-homes/details/52124564
16  2d ago           680000  NW1         Centric Close, Oval Road, London NW1            leasehold          1/1/     49.981814          13604.9   flat         https://zoopla.co.uk/new-homes/details/54216870
17  274d ago         699950  NW1         Kings Terrace, London NW1                       leasehold          2/1/1    76.18046            9188.05  flat         https://zoopla.co.uk/for-sale/details/48925648
18  68d ago          700000  NW1         Parkway, London NW1                             leasehold          2/2/1    80.918513           8650.68  flat         https://zoopla.co.uk/for-sale/details/51843171
19  29d ago          700000  NW1         Lyme Street, Camden, London NW1                 share_of_freehold  2/1/1    66.983063          10450.4   flat         https://zoopla.co.uk/for-sale/details/52504601
20  23d ago          725000  NW1         Royal College Street, London NW1                share_of_freehold  2/1/1    80.361095           9021.78  maisonette   https://zoopla.co.uk/for-sale/details/53993352
21  11d ago          750000  NW1         Oval Road, London NW1                                              2/2/1    68.004996          11028.6   flat         https://zoopla.co.uk/for-sale/details/54128543
22  29d ago          750000  NW1         Lyme Street, Camden, London NW1                 leasehold          2/1/1    83.333991           8999.93  flat         https://zoopla.co.uk/for-sale/details/53940681
23  72d ago          775000  NW1         Oval Road, London NW1                                              2/2/1    68.004996          11396.2   flat         https://zoopla.co.uk/for-sale/details/53557986
24  837d ago         800000  NW1         Parkway, Camden, London NW1                     leasehold          2/2/     NA                           flat         https://zoopla.co.uk/for-sale/details/39748209
25                   840000  NW1         Mode, Centric Close, Oval Road, Camden NW1                         2/1/1    NA                           flat         https://zoopla.co.uk/new-homes/details/51770636
26  205d ago         850000  NW1         Centric Close, Oval Road, London NW1            leasehold          2/2/     81.197222          10468.3   flat         https://zoopla.co.uk/new-homes/details/52170779
27  70d ago          850000  NW1         Centric Close, Oval Road, London NW1            leasehold          2/2/     81.475931          10432.5   flat         https://zoopla.co.uk/new-homes/details/52813965
28  168d ago         870000  NW1         Centric Close, Oval Road, London NW1            leasehold          2/2/     73.39337           11853.9   flat         https://zoopla.co.uk/new-homes/details/52535911
29  20d ago          875000  NW1         Camden Street, London NW1                       leasehold          2/1/1    96.061702           9108.73  maisonette   https://zoopla.co.uk/for-sale/details/48398820
30  70d ago          890000  NW1         Centric Close, Oval Road, London NW1            leasehold          2/1/     74.694012          11915.3   flat         https://zoopla.co.uk/new-homes/details/52123505
31  9d ago           950000  NW1         Bonny Street, Camden NW1                        freehold           4/1/2    40.784417          23293.2   terraced     https://zoopla.co.uk/for-sale/details/54135589
32  120d ago         950000  NW1         Arlington Road, London NW1                      leasehold          2/1/1    NA                           flat         https://zoopla.co.uk/for-sale/details/52856459
33  120d ago         950000  NW1         Arlington Road, Camden, London NW1              leasehold          2/2/1    106.559741          8915.19  flat         https://zoopla.co.uk/for-sale/details/52899610
34  118d ago         995000  NW1         Pratt Mews, Camden, London NW1                  leasehold          3/3/1    10.126427          98257.8   flat         https://zoopla.co.uk/new-homes/details/53065300
35  127d ago        1000000  NW1         Oval Road, London NW1                           leasehold          2//      73.021758          13694.5   flat         https://zoopla.co.uk/for-sale/details/52829038
36  120d ago        1000000  NW1         Henson Building, 30 Oval Road, London NW1       leasehold          2/2/1    73.021758          13694.5   flat         https://zoopla.co.uk/for-sale/details/53035315
37  141d ago        1000000  NW1         Lock House, Oval Road, London NW1               leasehold          2/2/1    76.737878          13031.4   flat         https://zoopla.co.uk/for-sale/details/52332024
38  114d ago        1000000  NW1         Oval Road, Camden, London NW1                                      2/2/1    76.923684          12999.9   flat         https://zoopla.co.uk/for-sale/details/53076887
39  291d ago        1075000  NW1         Regent Canalside, Camden Road, Camden Town NW1  leasehold          2/2/1    NA                           flat         https://zoopla.co.uk/for-sale/details/44538652
40  253d ago        1075000  NW1         Regent Canalside, Camden Road, London NW1                          2/2/1    NA                           flat         https://zoopla.co.uk/new-homes/details/52332025
41                  1100000  NW1         Mode, Centric Close, Oval Road, Camden NW1                         3/2/1    88.908171          12372.3   flat         https://zoopla.co.uk/new-homes/details/51770638
42                  1100000  NW1         Darwin Court, Camden Town, London NW1                              2/2/     112.226824          9801.58  flat         https://zoopla.co.uk/for-sale/details/49889322
43  210d ago        1100000  NW1         Centric Close, Oval Road, London NW1            leasehold          3/2/     88.908171          12372.3   flat         https://zoopla.co.uk/new-homes/details/52123426
44                  1100000  NW1         Regent Canalside, 37 Camden Road, London NW1    leasehold          3/3/1    118.91584           9250.24  flat         https://zoopla.co.uk/new-homes/details/53713638
45  140d ago        1150000  NW1         Albert Street, Camden, London NW1               leasehold          2/1/1    86.492693          13295.9   maisonette   https://zoopla.co.uk/for-sale/details/48405917
46  257d ago        1699950  NW1         Arlington Road, Camden, London NW1              freehold           4/2/2    145.207389         11707     terraced     https://zoopla.co.uk/for-sale/details/45238336
47                  1750000  NW1         Arlington Road, London, Camden NW1              freehold           4/2/2    176.701506          9903.71  terraced     https://zoopla.co.uk/for-sale/details/51734721
48  30d ago         1750000  NW1         Arlington Road, Camden, London NW1              freehold           4/2/2    212.562064          8232.89  terraced     https://zoopla.co.uk/for-sale/details/50718067
49  489d ago        1750000  NW1         Ivor Street, London NW1                         freehold           6/3/2    158.41912463       11046.6   terraced     https://zoopla.co.uk/for-sale/details/52332026
50  8d ago          2395000  NW1         Inverness Street, Camden Town, London NW1       freehold           4/2/2    180.696335         13254.3   end_terrace  https://zoopla.co.uk/for-sale/details/54152976
51  34d ago         3850000  NW1         Regents Park Terrace, London NW1                                   6/2/4    276.107716         13943.8                https://zoopla.co.uk/for-sale/details/53888711
52  267d ago        3875000  NW1         Regents Park Terrace, Primrose Hill NW1         freehold           4/3/4    274.06385          14139     terraced     https://zoopla.co.uk/for-sale/details/51514501
```
