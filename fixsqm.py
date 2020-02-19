import os
import json

for fname in os.listdir(".zoopler"):
    if not fname.endswith("house"):
        continue
    print(fname)
    with open(fname, "rb+") as f:
        print(f.read())
        f.seek(0)
        j = json.loads(f.read())
        if j["sqm"] != "NA":
            j["sqm"] = float(j["sqm"])
            j["ppsqm"] = j["price"] / j["sqm"]
            f.write(json.dumps(j))
            f.flush()
