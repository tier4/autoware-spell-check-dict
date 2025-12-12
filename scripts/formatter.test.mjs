import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { formatCspellJson, stringifyCspellJson } from "./formatter.mjs";

const input = readFileSync(
  new URL("./fixtures/.cspell.input.json", import.meta.url),
  "utf-8",
);
const expected = readFileSync(
  new URL("./fixtures/.cspell.answer.json", import.meta.url),
  "utf-8",
);

test("formatCspellJson formats correctly", () => {
  const inputJson = JSON.parse(input);
  const expectedJson = JSON.parse(expected);
  const formatted = formatCspellJson(inputJson);
  assert.deepStrictEqual(formatted, expectedJson);
});

test("stringified output matches expected", () => {
  const inputJson = JSON.parse(input);
  const formatted = formatCspellJson(inputJson);
  const formattedStr = stringifyCspellJson(formatted);
  assert.strictEqual(formattedStr, expected);
});
