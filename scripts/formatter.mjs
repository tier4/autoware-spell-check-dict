// Copyright 2022 TIER IV, Inc. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// cspell: ignore casefold
/**
 * Comparison function to sort strings in a list.
 * Reproduces the behavior of Python's (str.casefold(s), s).
 * 1. Compare by lowercased string.
 * 2. If equal, compare by original string.
 */
function sortStringsCaseInsensitive(a, b) {
  const lowerA = a.toLowerCase();
  const lowerB = b.toLowerCase();
  if (lowerA < lowerB) return -1;
  if (lowerA > lowerB) return 1;
  if (a < b) return -1;
  if (a > b) return 1;
  return 0;
}

/**
 * Recursively format a JSON object.
 * - dict(object): Recursive processing.
 * - list(array):
 * - If all elements are strings: Deduplicate (set) and sort.
 * - Otherwise: Recursive processing.
 */
function formatJsonRecursive(j) {
  if (Array.isArray(j)) {
    const isAllStrings = j.every((v) => typeof v === "string");
    if (!isAllStrings) {
      return j.map((v) => formatJsonRecursive(v));
    } else {
      // Deduplicate (set)
      const uniqueList = [...new Set(j)];
      // Sort
      return uniqueList.sort(sortStringsCaseInsensitive);
    }
  } else if (j !== null && typeof j === "object") {
    const newObj = {};
    for (const [k, v] of Object.entries(j)) {
      newObj[k] = formatJsonRecursive(v);
    }
    return newObj;
  }
  return j;
}

/**
 * Reconstruct the object based on the specified key order.
 * If keys exist in 'd' but not in 'newKeys', a warning is displayed,
 * and those keys are excluded from the result (matching original Python behavior).
 * * @param {Object} d - The dictionary to sort
 * @param {string[]} newKeys - The list of allowed keys in order
 * @param {string} [context] - Optional context name for logging (e.g. "root", "overrides")
 */
function sortDictKeys(d, newKeys, context = "unknown section") {
  const reorganized = {};

  // Rebuild object with allowed keys
  for (const key of newKeys) {
    if (d[key] !== undefined) {
      reorganized[key] = d[key];
    }
  }

  // Check for unknown keys and warn
  const existingKeys = Object.keys(d);
  const allowedKeysSet = new Set(newKeys);
  const unknownKeys = existingKeys.filter((k) => !allowedKeysSet.has(k));

  if (unknownKeys.length > 0) {
    // Attempt to identify the object for better logging (e.g., via languageId or filename)
    let identifier = "";
    if (d.languageId) identifier = ` (languageId: ${d.languageId})`;
    else if (d.filename) identifier = ` (filename: ${d.filename})`;

    console.warn(
      `[Warning] The following keys in "${context}"${identifier} are not in the allowed list and will be removed: [${unknownKeys.join(
        ", ",
      )}]`,
    );
  }

  return reorganized;
}

export function formatCspellJson(cspellJson) {
  // Recursively format internal values
  let formatted = formatJsonRecursive(cspellJson);

  // Sort top-level keys
  formatted = sortDictKeys(
    formatted,
    [
      "version",
      "language",
      "allowCompoundWords",
      "ignorePaths",
      "ignoreRegExpList",
      "import",
      "dictionaries",
      "languageSettings",
      "overrides",
      "flagWords",
      "words",
    ],
    "root",
  );

  // Sort inside "languageSettings"
  if (formatted.languageSettings) {
    // Sort items by languageId
    formatted.languageSettings.sort((a, b) => {
      if (a.languageId < b.languageId) return -1;
      if (a.languageId > b.languageId) return 1;
      return 0;
    });

    // Sort keys within each item
    formatted.languageSettings = formatted.languageSettings.map((d) =>
      sortDictKeys(
        d,
        ["languageId", "dictionaries", "ignoreRegExpList"],
        "languageSettings",
      ),
    );
  }

  // Sort inside "overrides"
  if (formatted.overrides) {
    // Sort items by filename
    formatted.overrides.sort((a, b) => {
      if (a.filename < b.filename) return -1;
      if (a.filename > b.filename) return 1;
      return 0;
    });

    // Sort keys within each item
    formatted.overrides = formatted.overrides.map((d) =>
      sortDictKeys(d, ["filename", "ignoreRegExpList"], "overrides"),
    );
  }

  return formatted;
}

export function stringifyCspellJson(cspellJson) {
  return JSON.stringify(cspellJson, null, 2) + "\n";
}
