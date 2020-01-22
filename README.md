# rac_aspace

*Write a brief description of the project, explaining what it does in a couple of sentences.*

## Functionality

### Data Helpers


### Serialize


### Save in ArchivesSpace


### Delete in ArchivesSpace

RAC_ASpace takes the fetched data from the helpers and simplifies delete actions. This could include deletion of an entire repository, resource, archival object, or deleting a single value in one of the JSON arrays. The key functionality differentiates between the deletion of a first-class ArchivesSpace object (which requires a delete request) and deletion of a field value (which requires data deletion and then a push request).

*   Deletion of first-class ArchivesSpace objects will require a Delete request against specific ArchivesSpace API endpoints, including, but not limited to, archival_objects, agents (corporate, person, family, software), subjects, top_containers, resources, and accessions.
*   Deleting field values in ArchivesSpace through the API requires getting a JSON package, modifying or deleting values, and then pushing that data back to ArchivcesSpace. This method uses the data helpers to quickly move between abstraction and client layers of ASnake to get object JSON as needed, deletes necessary values, and sends a Push request back to first-class endpoints using the ArchivesSpace API. 

RAC_ASpace also simplifies the deletion of unlinked objects in ArchivesSpace. The Delete_Orphans method will automatically identify unlinked agents, subjects, top containers, and digital objects in your ArchivesSpace database and delete them. This will help you keep your database clean after batch modification efforts.

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
