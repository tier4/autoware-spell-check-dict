# Copyright 2022 Tier IV, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
from pathlib import Path


# The key contained in the json.
# The default setting is {unique: False, sort: False, key_order: None}
KEYS = {
    "ignorePaths": {"unique": True, "sort": True, "key_order": None},
    "words": {"unique": True, "sort": True, "key_order": str.lower},
}


def unique_json(data, key):
    if key in data:
        data[key] = list(set(data[key]))
    return data


def sort_json(data, key, key_order=None):
    if key in data:
        data[key] = sorted(data[key], key=key_order)
    return data


def parse(data):
    for key in KEYS:
        if KEYS[key]["unique"]:
            data = unique_json(data, key)
        if KEYS[key]["sort"]:
            data = sort_json(data, key, key_order=KEYS[key]["key_order"])
    return data


def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    return_code = 0
    for filename in args.filenames:
        filepath = Path(filename)
        original_json = json.loads(filepath.read_text(encoding="utf-8"))
        original_json_str = json.dumps(original_json)

        sorted_json = parse(original_json)

        if json.dumps(sorted_json) != original_json_str:
            print(f"Fixing {filepath}")
            filepath.write_text(
                json.dumps(sorted_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            return_code = 1

    return return_code


if __name__ == "__main__":
    exit(main())
