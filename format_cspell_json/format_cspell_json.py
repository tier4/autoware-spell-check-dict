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
from typing import Dict, Optional, Sequence


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


def format_cspell_json(cspell_json: Dict) -> Dict:
    # Sort inside each key
    formatted = format_json_recursive(cspell_json)

    # Sort top-level keys
    new_keys = [
        "version",
        "language",
        "allowCompoundWords",
        "ignorePaths",
        "ignoreRegExpList",
        "overrides",
        "flagWords",
        "words",
    ]
    reorganized = {}
    for key in new_keys:
        if formatted.get(key) is not None:
            reorganized[key] = formatted[key]

    # Sort inside "overrides"
    reorganized["overrides"] = sorted(reorganized["overrides"], key=lambda x: x["filename"])

    return reorganized


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", type=Path, help="Filenames to fix")
    args = parser.parse_args(argv)

    return_code = 0
    for filepath in args.filenames:
        original_json = json.loads(filepath.read_text(encoding="utf-8"))
        sorted_json = format_cspell_json(copy.deepcopy(original_json))

        if json.dumps(sorted_json) != json.dumps(original_json):
            print(f"Fixing {filepath}")
            filepath.write_text(
                json.dumps(sorted_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            return_code = 1

    return return_code


if __name__ == "__main__":
    exit(main())
