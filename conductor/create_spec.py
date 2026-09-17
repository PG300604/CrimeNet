"""
Initialize APISpec
"""
import sys
sys.path.insert(0, "")
# import faulthandler
import ujson
from os.path import join, abspath, dirname
from conductor.src.config_spec import spec

output_path = "../conductor_docs/swagger/apispec.json"

with open(join(dirname(abspath(__file__)), output_path), "w+") as f:
    ujson.dump(
        spec.to_dict(),
        f,
        indent=4)
