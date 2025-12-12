#!/usr/bin/env node

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

import fs from "node:fs";
import { formatCspellJson, stringifyCspellJson } from "./formatter.mjs";

function main() {
  const args = process.argv.slice(2);
  let returnCode = 0;

  for (const filepath of args) {
    try {
      const originalJsonStr = fs.readFileSync(filepath, "utf-8");
      const originalJson = JSON.parse(originalJsonStr);

      // Deep copy before formatting
      const inputCopy = JSON.parse(JSON.stringify(originalJson));
      const sortedJson = formatCspellJson(inputCopy);

      // Add indentation of 2 spaces and a newline at the end
      const sortedJsonStr = stringifyCspellJson(sortedJson);

      if (sortedJsonStr !== originalJsonStr) {
        console.log(`Fixing ${filepath}`);
        fs.writeFileSync(filepath, sortedJsonStr, "utf-8");
        returnCode = 1;
      }
    } catch (err) {
      console.error(`Error processing ${filepath}:`, err.message);
      returnCode = 1;
    }
  }

  process.exit(returnCode);
}

main();
