import { spellCheckDocument } from "cspell-lib";
import { formatCspellJson } from "./formatter.mjs";
import fs from "fs/promises";

async function checkSpelling(phrase, config) {
  const result = await spellCheckDocument(
    { uri: "text.txt", text: phrase, languageId: "plaintext", locale: "en" },
    { generateSuggestions: true, noConfigSearch: true },
    config
  );
  return result.issues;
}

async function main() {
  const configPath = process.argv[2];

  if (!configPath) {
    console.error("Usage: node cleanup_cspell.mjs <path-to-cspell-config>");
    process.exit(1);
  }

  const config = JSON.parse(await fs.readFile(configPath, "utf-8"));
  const customWords = new Set(config.words || []);
  const noCustomWordsConfig = { ...config, words: [] };

  const testPhrases = config.words.join("\n");
  const issues = await checkSpelling(testPhrases, noCustomWordsConfig);

  const misspelledWords = new Set(issues.map((issue) => issue.text));
  const falsePositives = config.words.filter((word) => !misspelledWords.has(word));

  if (falsePositives.length > 0) {
    console.log("Removing false positive words:");
    falsePositives.forEach((word) => console.log(`- ${word}`));
    falsePositives.forEach((word) => customWords.delete(word));
  }

  const cleanedConfig = { ...config, words: Array.from(customWords).sort() };
  const formattedConfig = formatCspellJson(cleanedConfig);
  await fs.writeFile(configPath, JSON.stringify(formattedConfig, null, 2), "utf-8");
}

main();
