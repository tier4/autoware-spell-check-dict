#!/usr/bin/env bash

echo "Sorting cspell json files"
echo "Target file is $1"

# Install jq
if ! (command -v jq >/dev/null 2>&1); then
    echo "Installing jq"
    sudo apt-get install -y jq
fi

# Set target file
cspell_json="$1"

# Create new json
sorted_json=$(
    jq --indent 2 \
        "{
        version: .version,
        language: .language,
        allowCompoundWords: .allowCompoundWords,
        languageSettings: .languageSettings,
        overrides: .overrides,
        ignorePaths: .ignorePaths | sort_by(.),
        ignoreRegExpList: .ignoreRegExpList,
        flagWords: .flagWords,
        words: .words | unique | sort_by(. | ascii_downcase),
    }" <"$cspell_json"
)

# If jq succeed, replace file
if [ "${PIPESTATUS[0]}" = "0" ]; then
    echo "Sorting succeeded"
    echo "$sorted_json" >"$cspell_json"
else
    echo "Failed to parse json."
    exit 1
fi
