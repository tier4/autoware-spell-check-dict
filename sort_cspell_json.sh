#!/usr/bin/env bash

SCRIPT_DIR=$(readlink -e "$(dirname "${0}")")

# Install jq
if ! (command -v jq > /dev/null 2>&1); then
    sudo apt-get install -y jq
fi

# Set target file
cspell_json="$SCRIPT_DIR/cspell/.cspell.json"

# Create new json
sorted_json=$(jq --indent 4 \
    "{
        version: .version,
        language: .language,
        allowCompoundWords: .allowCompoundWords,
        languageSettings: .languageSettings,
        overrides: .overrides,
        ignorePaths: .ignorePaths | sort_by(.),
        flagWords: .flagWords,
        words: .words | unique | sort_by(. | ascii_downcase),
    }" < "$cspell_json"
)

# If jq succeed, replace file
if [ "${PIPESTATUS[0]}" = "0" ]; then
    echo "$sorted_json" > "$cspell_json"
else
    echo "Failed to parse json."
    exit 1
fi
