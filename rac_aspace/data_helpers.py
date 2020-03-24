"""Data Helpers

Data helpers leverage the abstraction layer of ArchivesSnake to provide
additional functionality for retrieving, inferring and concatenating data
elements. They can also extend (or invert) relationships between different
objects.

"""
import re
from fuzzywuzzy import fuzz
from decorators import (check_dictionary, check_list, check_str)


@check_dictionary
def get_note_text(note):
    """Parses note content from different note types.

    Args:
        note (dict): an ArchivesSpace note object.

    Returns:
        list: a list containing note content.
    """
    def parse_subnote(subnote):
        """Parses note content from subnotes.

        Args:
            subnote (dict): an ArchivesSpace subnote object.

        Returns:
            list: a list containing subnote content.
        """
        if subnote.jsonmodel_type in [
                'note_orderedlist', 'note_definedlist', 'note_index',
                'note_chronology']:
            content = subnote.items
        elif subnote.jsonmodel_type == 'note_bibliography':
            data = []
            data.append(subnote.content)
            data.append(subnote.items)
            content = data
        else:
            content = subnote.content if isinstance(
                subnote.content, list) else [subnote.content]
        return content

    if note.jsonmodel_type == "note_singlepart":
        content = note.content
    elif note.jsonmodel_type == "note_index":
        content = note.items
    else:
        subnote_content_list = list(parse_subnote(sn) for sn in note.subnotes)
        content = [
            c for subnote_content in subnote_content_list for c in subnote_content]
    return content


@check_dictionary
def text_in_note(note, query_string):
    """Performs fuzzy searching against note text.

    Args:
        note (dict): an ArchivesSpace note object.
        query_string (str): a string to match against.

    Returns:
        bool: True if a match is found for `query_string`, False if no match is
            found.
    """
    CONFIDENCE_RATIO = 97
    """int: Minimum confidence ratio to match against."""
    note_content = get_note_text(note)
    ratio = fuzz.token_sort_ratio(
        " ".join([n.lower() for n in note_content]), query_string.lower())
    return (True if ratio > CONFIDENCE_RATIO else False)


@check_dictionary
def get_locations(archival_object):
    """Finds locations associated with an archival object.

    Args:
        archival_object (dict): an ArchivesSpace archival_object.

    Returns:
        list: Locations objects associated with the archival object.
    """
    locations = []
    for instance in archival_object.instances:
        locations.append(instance.top_container.location)
    return locations


@check_dictionary
def format_location(location):
    """Generates a human-readable string describing a location.

    Args:
        location (dict): an ArchivesSpace location object.

    Returns:
        str: a string representing the location
    """
    pass
# QUESTION: pass a format string
# QUESTION: is this a more generalizable function?
# grab fields from location
# format string "{} {}, {}-{}"
# return format string


@check_dictionary
def format_container(top_container):
    """Generates a human-readable string describing a container.

    Args:
        top_container (dict): an ArchivesSpace top_container object.

    Returns:
        str: a concatenation of top container type and indicator.
    """
    return "{0} {1}".format(top_container.type,
                            top_container.indicator)


@check_dictionary
def format_resource_id(resource, separator=":"):
    """Concatenates the four-part ID for a resource record.

    Args:
        resource (dict): an ArchivesSpace resource object.
        separator (str): a separator to insert between the id parts. Defaults
            to `:`.

    Returns:
        str: a concatenated four-part ID for the resource record.
    """
    resource_id = []
    for x in range(4):
        try:
            resource_id.append(getattr(resource, "id_{0}".format(x)))
        except AttributeError:
            break
    return separator.join(resource_id)


@check_dictionary
def closest_value(archival_object, key):
    """Finds the closest value matching a key.

    Starts with an archival object, and iterates up through it's ancestors
    until it finds a match for a key that is not empty or null.

    Args:
        archival_object (dict): an ArchivesSpace archival_object
        key (str): the key to match against.

    Returns:
        The value of the key, which could be a str, list, or dict
    """
    if getattr(archival_object, key) not in ['', [], {}, None]:
        return archival_object.key
    else:
        for ancestor in archival_object.ancestors:
            return closest_value(ancestor, key)


@check_list
def get_orphans(object_list, null_attribute):
    """Finds objects in a list which do not have a value in a specified field.

    Args:
        object_list (list): a list of ArchivesSpace objects.
        null_attribute: an attribute which must be empty or null.

    Yields:
        dict: a list of ArchivesSpace objects.
    """
    for obj in object_list:
        if getattr(obj, null_attribute) in ['', [], {}, None]:
            yield obj


@check_dictionary
def get_expression(date):
    """Returns a date expression for a date object.

    Concatenates start and end dates if no date expression exists.

    Args:
        date (obj): an ArchivesSpace date object

    Returns:
        str: a date expression for the date object.
    """
    date_json = date.json()
    try:
        expression = date_json["expression"]
    except KeyError:
        if date_json.get("end"):
            expression = "{0}-{1}".format(date_json["begin"], date_json["end"])
        else:
            expression = date_json["begin"]
    return expression


@check_dictionary
def associated_objects(top_container):
    """Returns all archival objects associated with a top container.

    Args:
        top_container (dict): an ArchivesSpace top_container object.

    Returns:
        list: a list of associated archival objects.
    """
    pass
# probably have to do some SOLR stuff


@check_dictionary
def indicates_restriction(rights_statement):
    """Parses a rights statement to determine if it indicates a restriction.

    Args:
        rights_statement (dict): an ArchivesSpace rights statement.

    Returns:
        bool: True if rights statement indicates a restriction, False if not.
    """
    # If rights_statement.date_end is before today:
    # return False
    # for rights_granted in rights_statement.rights_granted:
    # if rights_granted.date_end is after today:
    # if rights_granted.act in ["disallow", "conditional"]:
    # return True
    # return False

@check_dictionary
def is_restricted(archival_object):
    """Parses an archival object to determine if it is restricted.

    Iterates through notes, looking for a conditions governing access note
    which contains a particular set of strings.
    Also looks for associated rights statements which indicate object may be
    restricted.

    Args:
        archival_object (dict): an ArchivesSpace archival_object.

    Returns:
        bool: True if archival object is restricted, False if not.
    """
    query_string = "materials are restricted"
    for note in archival_object.notes:
        if note.type == 'accessrestrict':
            if text_in_note(note, query_string):
                return True
    for rights_statement in archival_object.rights_statements:
        if indicates_restriction(rights_statement):
            return True
    return False


@check_str
def strip_html_tags(string):
    """Strips HTML tags from a string.

    Args:
        string (str): An input string from which to remove HTML tags.
    """
    tag_match = re.compile('<.*?>')
    cleantext = re.sub(tag_match, '', string)
    return cleantext
