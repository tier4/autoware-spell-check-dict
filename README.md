# autoware-spell-check-dict

## Description

An Autoware-specific word dictionary for spell checking.

The dictionary contains some words which are found in documents and source code of Autoware, but not in common English dictionaries.

The words in the dictionary are sorted by the command `sort --ignore-case | uniq`.

## How to contribute

Just edit `.cspell.json` as follows and send a pull-request to this repository. Thanks!

The words you inserted into the json will be **sorted automatically** by GitHub Actions or pre-commit hook (if you set it up).

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

### Automatic cleanup of unused words

With the [autoclean workflow](https://github.com/autowarefoundation/autoware-spell-check-dict/actions/workflows/autoclean.yaml), automated Pull Requests are created to remove unused words from `.cspell.json`.

### Update upstream dictionaries

In `package.json`, the following upstream dictionaries are used as dependencies.

- `@cspell/dict-en-gb`
- `@cspell/cspell-bundled-dicts`
- (`@tier4/cspell-dicts`: Provided by GitHub repository)

To update them, run the following command and send a pull-request to this repository.

```shell
npm update @cspell/dict-en-gb @cspell/cspell-bundled-dicts
```

## How to check spelling with the dictionary in your local environment

### Ubuntu 22.04 or later

**Requirement**: Node.js >= v20

```shell
# Install Node.js
# See the latest instruction https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions
# The following command installs Node.js LTS
$ curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
$ sudo apt install nodejs

# Make sure that Node.js >= v20
$ node -v
v24.4.1

# Install cspell and autoware-spell-check-dict as a global package from GitHub
$ npm install -g cspell https://github.com/autowarefoundation/autoware-spell-check-dict

# Check spelling
$ cspell -c '@tier4/autoware-spell-check-dict/.cspell.json' /path/to/src/*.cpp /path/to/include/*.hpp

# Check all files using glob patterns
$ cspell -c '@tier4/autoware-spell-check-dict/.cspell.json' '**/*.{cpp,hpp,xml,md}'

# Alternative way: Using npm exec without global installation
$ npx --package cspell --package https://github.com/autowarefoundation/autoware-spell-check-dict cspell -c '@tier4/autoware-spell-check-dict/.cspell.json' '**/*.{cpp,hpp,xml,md}'
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
