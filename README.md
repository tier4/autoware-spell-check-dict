# autoware-spell-check-dict

## Description

An Autoware-specific word dictionary for spell checking.

The dictionary contains some words which are found in documents and source code of Autoware, but not in common English dictionaries.

The words in the dictionary are sorted by the command `sort --ignore-case | uniq`.

## How to contribute

Just edit `cspell/.cspell.json` as follows and send a pull-request to this repository. Thanks!

The words you inserted into the json will be **sorted automatically** by GitHub Actions.

```json
{
    "words": [
        "add-word1-here",
        "add-word2-here",
        "add-word3-here",
        "aarch",
        "abstractmethod",
        "..."
    ]
}
```

## How to check spelling with the dictionary in your local environment

### Ubuntu 18.04 or later

```shell
# Install a spell checker (cspell) using npm
$ sudo apt install nodejs
$ sudo npm install -g cspell

# Copy the dictionary into your environment
$ cd /your-project-dir
$ wget https://raw.githubusercontent.com/tier4/autoware-spell-check-dict/main/cspell/.cspell.json

# Check spelling
$ cspell /path/to/src/*.cpp /path/to/include/*.hpp

# Or
$ find . -name '*.cpp' -o -name '*.hpp' -o -name '*.xml' -o -name '*.md' | xargs cspell

# Or
$ find . -type d -name '.git' -prune -o \
         -type d -name 'vendor' -prune -o \
         -type f -name '*' \
         -not -name '*onnx' \
         -not -name '*.cu' \
         -not -name '*.pcd' \
         -not -name '*cspell*' \
         -not -name '*compile_commands.json' \
         -not -name '*.caffemodel' \
         -not -name '*.svg' \
         -not -name '*.pcd' \
          | xargs cspell > cspell_all
```

### VSCode

Please use [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker) and be sure to add the followings to `settings.json`.

```json
"cSpell.languageSettings": [
    {
        "languageId": "c,cpp,python",
        "allowCompoundWords": false
    }
]
```
