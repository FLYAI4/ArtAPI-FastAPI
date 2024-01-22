import os
import json

apps_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
conf_path = os.path.abspath(os.path.join(apps_path, "conf"))

conf_file = os.path.abspath(os.path.join(conf_path, "conf.json"))
with open(conf_file, "rt") as f:
    conf = json.load(f)
