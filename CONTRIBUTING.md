# Contributing

See <https://autowarefoundation.github.io/autoware-documentation/main/contributing/>.

## How to judge whether to add a word?

Please follow the flowchart below.

<img alt="judgement_flowchart" src="image/judgement_flowchart.drawio.svg" width="50%">

The link to cspell-dicts: [here](https://github.com/tier4/cspell-dicts)

If the above flowchart still doesn't provide a clear answer, please consider the following:

- **Frequency of use**: Is the word used in various locations around the world, or is it common in a specific specialized industry?
- **Necessity for the Autoware Foundation**: Is the word necessary to use in autoware? Is the word used by the maintainers?

In other cases, please consult the maintainers of this repository. For example:

- A word like `nocuda`, which should be split but is frequently used in the names of Docker images.
- Code from external packages that has been copied and pasted to be used as a library, and you don't want to change it to keep the differences clear.
