# autoware-spell-check-dict

## Description

An Autoware-specific word dictionary for spell checking.

The dictionary contains some words which are found in documents and source code of Autoware, but not in common English dictionaries.

The words in the dictionary are sorted by the command `sort --ignore-case | uniq`.

## How to contribute

Just edit `.cspell.json` as follows and send a pull-request to this repository. Thanks!

The words you inserted into the json will be **sorted automatically** by GitHub Actions.

```json
{
  "words": [
    "add-word1-here",
    "add-word2-here",
    "add-word3-here",
    "aarch",
    "abstractmethod",
    "...",
    "..."
  ]
}
```

### Easy-to-add a word using workflow

With the [add-word workflow](https://github.com/tier4/autoware-spell-check-dict/actions/workflows/add-word.yaml), you can create a pull request to add a word to `.cspell.json`.

![image](https://user-images.githubusercontent.com/12395284/232272339-ec5edcee-cc67-45a8-badc-fc4edb7d9390.png)

## How to check spelling with the dictionary in your local environment

### Ubuntu 18.04 or later

**Requirement**: Node.js >= v12

```shell
# Install Node.js
# See the latest instruction https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions
# The following command installs Node.js LTS
$ curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
$ sudo apt install nodejs

# Make sure that Node.js >= v12
$ node -v
v16.13.0

# Install a spell checker (cspell) using npm
$ sudo npm install -g cspell

# Install additional dictionaries
$ npm install -g yarn
$ yarn global add https://github.com/tier4/cspell-dicts

# Copy the dictionary into your environment
$ cd /your-project-dir
$ wget -O .cspell.json https://raw.githubusercontent.com/tier4/autoware-spell-check-dict/main/.cspell.json

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

### Visual Studio Code

Please install [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker) and be sure to add the followings to `settings.json`.

```json
"cSpell.languageSettings": [
    {
        "languageId": "c,cpp,python",
        "allowCompoundWords": false
    }
]
```
