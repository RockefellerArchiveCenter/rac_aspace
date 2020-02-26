# rac_aspace

*Write a brief description of the project, explaining what it does in a couple of sentences.*

## Functionality

### Data Helpers

Target, extract, and modify structured data from ArchiveSpace to allow users to export, update, add, and delete data. Data helpers leverage the abstraction layer of ArchivesSnake to get and post changes back to a JSONModel object(s) either in bulk, or by specifying a unique identifier. Data helpers enable cleanup tasks, changes to conform to new organizational policies and procedures, and to validate against existing archival and institutional standards. Data helper functionality includes:

#### Retrieve
Get specific fields from a data object.

- ~~Notes attached to archival objects or resources~~ see `of_type()` and `get_note_text()`
- ~~Location data~~ see `get_locations()`
- Container data
- Date data
- ~~Data fields within an AS object, including arrays within arrays~~ see conversation about list comprehension
- ~~Unlinked agents, subjects, top containers, and digital objects~~ see `get_orphans()`

#### Infer
Return properties based on other data elements, either on the same object or another.

- ~~Date expression based on date type and start/end dates~~ see `expression()`
- ~~List of all the restricted archival objects associated with a given top container~~ see `text_in_note()` and `is_restricted()` and `indicates_restriction()`
- see also `closest_value()`

#### Extend relationships
Find related objects which are not related via `ref` properties (and so cannot be traversed in the ASpace abstraction layer)

- ~~Archival objects associated with a top container~~ see `associated_objects()` 

#### Concatenate Fields
Combine discrete data elements to form a single value.

- ~~Container type plus identifier~~ see `format_container()`
- ~~Four-part id (id_0 plus id_1 plus id_2 plus id_3)~~  see `format_resource_id()`
- ~~Note content. Depending on note type, this requires iterating through subnotes.~~ see `get_note_text()`
- see also `format_location()`

#### Enable User Input

- ~~To target specific objects and resources in order to retrieve or modify data~~ see `get_user_input()`
- ~~For initial setup of local configurations~~ see `get_config()`

### Serialize

Simplify and standardize writing ArchivesSpace data obtained from the data helpers to an external tabular data serialization. Serialization formats should include CSV and TSV, and enable setup with column headings and the naming of output files.

Serializing tabular data from ArchivesSpace enables the repurposing, editing, manipulation, and evaluation of the data.


### Save in ArchivesSpace

The RAC_ASpace library improves upon the ArchivesSnake saving functionality by generalizing processes and making it easier to save new JSON data and push that back up to ArchivesSpace.

We plan to do that by:
  * Generalizing the transformation from a JSONModel object fetched by ArchivesSnake to editable JSON
  * Making Create and Update methods for pushing new or updated JSON data back to ArchivesSpace

### Delete in ArchivesSpace

RAC_ASpace takes the fetched data from the helpers and simplifies delete actions. This could include deletion of an entire repository, resource, archival object, or deleting a single value in one of the JSON arrays. The key functionality differentiates between the deletion of a first-class ArchivesSpace object (which requires a delete request) and deletion of a field value (which requires data deletion and then a push request).

*   Deletion of first-class ArchivesSpace objects will require a Delete request against specific ArchivesSpace API endpoints, including, but not limited to, archival_objects, agents (corporate, person, family, software), subjects, top_containers, resources, and accessions.
*   Deleting field values in ArchivesSpace through the API requires getting a JSON package, modifying or deleting values, and then pushing that data back to ArchivesSpace. This method uses the data helpers to quickly move between abstraction and client layers of ASnake to get object JSON as needed, delete necessary values, and send a Push request back to first-class endpoints using the ArchivesSpace API.

RAC_ASpace also simplifies the deletion of unlinked objects in ArchivesSpace. The Delete_Orphans method will automatically identify unlinked agents, subjects, top containers, and digital objects in an ArchivesSpace database and delete them. This will help keep the database clean after batch modification efforts.

## To Use

### Requirements

Add software operating systems, programming languages or libraries which are required by this project as an unordered list like this:

*   Python 3.4 or higher
*   [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake)
*   [tox](https://tox.readthedocs.io/) (for running tests)
*   [pre-commit](https://pre-commit.com/) (for running linters before committing)
    *   After installing pre-commit, install the git-hook scripts:

    ```
    $ pre-commit install
    ```

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

## Contributing

Contributions to rac_aspace are welcome, and all contributors will be acknowledged! Any contributions made to rac_aspace must be available for public distribution under the project’s MIT License.

### How to Contribute

  * Report a bug - Open a new issue. When prompted, select the Report Bug Issue Template and describe the bug encountered and any additional information.
  * Fix a bug - Search for issues related to bugs. Follow the instructions for contributing changes below.
  * Request a feature - Open a new issue. When prompted, select the Feature Request Issue Template and describe the proposed enhancement.
  * Implement a feature request - Search for issues related to feature requests. Follow instructions for contributing changes below.
  * You may contribute code for bugs or features that you have reported, just please file an issue first.

### Contributing Changes

In order to contribute changes, you must first set up rac_aspace for local development.

To do this:

  1. Fork the rac_ascpace GitHub repo
  2. Clone the fork locally
  3. Install requirements in `requirements.txt` (we recommend using [virtual](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to keep your dependencies isolated)
  4. Create a new branch, named after the issue number your work corresponds to
  5. Make changes and push your branch

After you have finished making your changes on the new branch, your code must pass all required tests before committing changes and follow the project’s conventions for submitting a pull request to the master branch on the rac_aspace GitHub repo.

To do this:

  1. Run unit tests and linters by consulting Tests section for instructions
  2. Commit changes to your working branch and push the branch to the rac_aspace GitHub
  3. Open a pull request against master and use the Pull Request Template to describe the changes you are contributing

Pull requests will be reviewed and merged by the rac_aspace maintainers.

### License

See`LICENSE.md`.
