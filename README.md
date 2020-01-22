# rac_aspace

*Write a brief description of the project, explaining what it does in a couple of sentences.*

## Functionality

### Data Helpers


### Serialize


### Save in ArchivesSpace


### Delete in ArchivesSpace


## To Use

### Requirements

Add software operating systems, programming languages or libraries which are required by this project as an unordered list like this:

*   Python 3.4 or higher
*   [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake)
*   [tox](https://tox.readthedocs.io/) (for running tests)

### Installation

*Describe the installation process, using `inline code blocks` to indicate terminal commands.*

### Usage

*Write usage instructions, including configuration details, settings or arguments available.*

#### Tests

`rac_aspace` comes with unit tests as well as linting. The easiest way to make sure all tests pass is to run `tox` from the root of the repository. This will execute all tests, and will also run `autopep8` and `flake8` linters against the codebase.

If you want to run a single unit test, you can also target a specific test file:

```
$ python tests/test_data_helpers.py
```

or you can run `autopep8` and `flake8` on their own:

```
$ autopep8 --in-place --aggressive -r .
$ flake8
```

### License

See`LICENSE.md`.
