import fs from "node:fs/promises";
import {
  type CSpellUserSettings,
  spellCheckDocument,
  type TextDocumentLine,
} from "cspell-lib";
import { formatCspellJson, stringifyCspellJson } from "./formatter.mjs";

async function checkSpelling(phrase: string, config: CSpellUserSettings) {
  const result = await spellCheckDocument(
    { uri: "text.md", text: phrase, languageId: "markdown" },
    {
      ...config,
      generateSuggestions: false,
      noConfigSearch: true,
    },
    {
      ...config,
      loadDefaultConfiguration: false,
      noConfigSearch: true,
      maxNumberOfProblems: 10000,
    },
  );
  const json = JSON.stringify(result, null, 2);
  await fs.writeFile("cspell-check-result.json", json, "utf-8");
  return result.issues;
}

async function main() {
  const configPath = process.argv[2];

  if (!configPath) {
    console.error("Usage: node cleanup_cspell.mjs <path-to-cspell-config>");
    process.exit(1);
  }

  const config: CSpellUserSettings = JSON.parse(
    await fs.readFile(configPath, "utf-8"),
  );

  // Deduplicate words in the custom dictionary
  const customWords = Array.from(new Set(config.words || []));

  // Check which words are still detected as misspelled in both original and lowercase forms
  const validateText = customWords
    .concat(customWords.map((word) => word.toLowerCase()))
    .join("\n");
  const spellIssues = await checkSpelling(validateText, {
    ...config,
    words: [],
  });

  const misspelledIndexes = new Set<number>();
  const warnings: string[] = [];
  for (const issue of spellIssues) {
    if (!("position" in issue.line)) {
      console.error(
        `Unexpected issue line format: ${JSON.stringify(issue.line)}`,
      );
      continue;
    }
    const line = issue.line as TextDocumentLine;
    const wordIndex = line.position.line % customWords.length;
    misspelledIndexes.add(wordIndex);

    if (
      issue.offset !== line.offset ||
      issue.text.length !== customWords[wordIndex].length
    ) {
      warnings.push(
        `Warning: \`${customWords[wordIndex]}\` is longer than detected word \`${issue.text}\` (maybe more than one word?)`,
      );
    }
  }

  const cleanedWords = customWords.filter((_, index) =>
    misspelledIndexes.has(index),
  );

  for (const [index, word] of customWords.entries()) {
    if (!misspelledIndexes.has(index)) {
      console.log(`Removed word: ${word}`);
    }
  }

  console.log(
    `Cleaned dictionary: ${
      customWords.length - cleanedWords.length
    } words removed.`,
  );

  for (const warning of warnings) {
    console.warn(warning);
  }

  const cleanedConfig = { ...config, words: Array.from(cleanedWords).sort() };
  const formattedConfig = formatCspellJson(cleanedConfig);
  await fs.writeFile(configPath, stringifyCspellJson(formattedConfig), "utf-8");
}

main();
