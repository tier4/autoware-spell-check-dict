# Copyright 2022 TIER IV, Inc. All rights reserved.
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
import copy
import json
from pathlib import Path
from typing import Dict, List, Optional, Sequence


# The keys contained in the JSON file.
# The default setting is {unique: False, sort: False, key_order: None}
KEYS = {
    "ignorePaths": {"unique": True, "sort": True, "key_order": None},
    "words": {"unique": True, "sort": True, "key_order": str.lower},
}


def unique_json(data: Dict[str, List[str]], key: str) -> Dict[str, List[str]]:
    unique_data = copy.deepcopy(data)
    if key in data:
        unique_data[key] = list(set(data[key]))
    return unique_data


def sort_json(data: Dict[str, List[str]], key: str, key_order: str = None) -> Dict[str, List[str]]:
    sorted_data = copy.deepcopy(data)
    if key in data:
        sorted_data[key] = sorted(data[key], key=key_order)
    return sorted_data


def format_cspell_json(cspell_json: Dict[str, List[str]]) -> Dict[str, List[str]]:
    formatted_json = copy.deepcopy(cspell_json)
    for key in KEYS:
        if KEYS[key]["unique"]:
            formatted_json = unique_json(formatted_json, key)
        if KEYS[key]["sort"]:
            formatted_json = sort_json(formatted_json, key, key_order=KEYS[key]["key_order"])
    return formatted_json


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", type=Path, help="Filenames to fix")
    args = parser.parse_args(argv)

    return_code = 0
    for filepath in args.filenames:
        original_json = json.loads(filepath.read_text(encoding="utf-8"))
        sorted_json = format_cspell_json(original_json)

        if json.dumps(sorted_json) != json.dumps(original_json):
            print(f"Fixing {filepath}")
            filepath.write_text(
                json.dumps(sorted_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            return_code = 1

    return return_code


if __name__ == "__main__":
    exit(main())
