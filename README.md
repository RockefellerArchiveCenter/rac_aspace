# rac_aspace

*Write a brief description of the project, explaining what it does in a couple of sentences.*

## Functionality

### Data Helpers

Target, extract, and modify structured data from ArchiveSpace to allow users to export, update, add, and delete data. Data helpers leverage the abstraction layer of ArchivesSnake to get and post changes back to a JSONModel object(s) either in bulk, or by specifying a unique identifier. Data helpers enable cleanup tasks, changes to conform to new organizational policies and procedures, and to validate against existing archival and institutional standards. Data helper functionality includes:

#### Retrieve and Modify

- Notes attached to archival objects or resources
- Location data
- Container data
- Date data
- Data fields within an AS object, including arrays within arrays
- Unlinked agents, subjects, top containers, and digital objects

#### Infer and Modify

- Date expression based on date type and start/end dates
- List of all the restricted archival objects associated with a given top container

#### Concatenate Fields

- Container type plus indentifier
- Four-part id (id_0 plus id_1 plus id_2 plus id_3)
- Note content. Depending on note type, this requires iterating through subnotes.

#### Enable User Input

- To target specfic objects and resources in order to retrieve or modify data
- For initial setup of local configurations

### Serialize


### Save in ArchivesSpace


### Delete in ArchivesSpace


## To Use

### Requirements

Add software operating systems, programming languages or libraries which are required by this project as an unordered list like this:

*   Python 3.4 or higher
*   [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake)

### Installation

*Describe the installation process, using `inline code blocks` to indicate terminal commands.*

### Usage

*Write usage instructions, including configuration details, settings or arguments available.*

### License

See`LICENSE.md`.