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
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence


def format_json_recursive(j: Dict) -> Dict:
    if isinstance(j, dict):
        j = {k: format_json_recursive(v) for k, v in j.items()}
    elif isinstance(j, list):
        if any([not isinstance(v, str) for v in j]):
            j = [format_json_recursive(v) for v in j]
        else:
            j = list(set(j))
            j = sorted(j, key=str.lower)
    return j


def sort_dict_keys(d: Dict, new_keys: List[str]):
    reorganized = {}
    for key in new_keys:
        if d.get(key) is not None:
            reorganized[key] = d[key]
    return reorganized


def format_cspell_json(cspell_json: Dict) -> Dict:
    # Sort inside each key
    formatted = format_json_recursive(cspell_json)

    # Sort top-level keys
    formatted = sort_dict_keys(
        formatted,
        [
            "version",
            "language",
            "allowCompoundWords",
            "ignorePaths",
            "ignoreRegExpList",
            "languageSettings",
            "overrides",
            "flagWords",
            "words",
        ],
    )

    # Sort inside "languageSettings"
    if formatted.get("languageSettings") is not None:
        # Sort items
        formatted["languageSettings"] = sorted(
            formatted["languageSettings"], key=lambda x: x["languageId"]
        )

        # Sort keys
        formatted["languageSettings"] = [
            sort_dict_keys(
                d,
                [
                    "languageId",
                    "dictionaries",
                    "ignoreRegExpList",
                ],
            )
            for d in formatted["languageSettings"]
        ]

    # Sort inside "overrides"
    if formatted.get("overrides") is not None:
        # Sort items
        formatted["overrides"] = sorted(formatted["overrides"], key=lambda x: x["filename"])

        # Sort keys
        formatted["overrides"] = [
            sort_dict_keys(
                d,
                [
                    "filename",
                    "ignoreRegExpList",
                ],
            )
            for d in formatted["overrides"]
        ]

    return formatted


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", type=Path, help="Filenames to fix")
    args = parser.parse_args(argv)

    return_code = 0
    for filepath in args.filenames:
        original_json_str = filepath.read_text(encoding="utf-8")
        original_json = json.loads(original_json_str)

        sorted_json = format_cspell_json(copy.deepcopy(original_json))
        sorted_json_str = json.dumps(sorted_json, indent=2, ensure_ascii=False) + "\n"

        if sorted_json_str != original_json_str:
            print(f"Fixing {filepath}")
            filepath.write_text(sorted_json_str, encoding="utf-8")
            return_code = 1

    return return_code


if __name__ == "__main__":
    exit(main())
