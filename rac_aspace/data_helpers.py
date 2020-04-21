"""Data Helpers

Data helpers leverage the abstraction layer of ArchivesSnake to provide
additional functionality for retrieving, inferring and concatenating data
elements. They can also extend (or invert) relationships between different
objects.

"""
from datetime import datetime
import re
from rapidfuzz import fuzz
from asnake.jsonmodel import JSONModelObject
from string import Formatter

from .decorators import check_type


# @check_type(dict)
def get_note_text(note):
    """Parses note content from different note types.

    Args:
        note (array): an ArchivesSpace note.

    Returns:
        list: a list containing note content.
    """
    def parse_subnote(subnote):
        """Parses note content from subnotes.

        Args:
            subnote (array): an ArchivesSpace subnote.

        Returns:
            list: a list containing subnote content.
        """
        if subnote['jsonmodel_type'] in [
                'note_orderedlist', 'note_index']:
            content = subnote['items']
        elif subnote['jsonmodel_type'] in ['note_chronology', 'note_definedlist']:
            content = []
            for k in subnote['items']:
                for i in k:
                    content += k.get(i) if isinstance(k.get(i),
                                                      list) else [k.get(i)]
        else:
            content = subnote['content'] if isinstance(
                subnote['content'], list) else [subnote['content']]
        return content

    if note['jsonmodel_type'] == "note_singlepart":
        content = note['content']
    elif note['jsonmodel_type'] == 'note_bibliography':
        data = []
        data += note['content']
        data += note['items']
        content = data
    elif note['jsonmodel_type'] == "note_index":
        data = []
        for item in note['items']:
            data.append(item['value'])
        content = data
    else:
        subnote_content_list = list(parse_subnote(sn)
                                    for sn in note['subnotes'])
        content = [
            c for subnote_content in subnote_content_list for c in subnote_content]
    return content


# @check_type(JSONModelObject)
def text_in_note(note, query_string):
    """Performs fuzzy searching against note text.

    Args:
        note (JSONModelObject): an ArchivesSpace note object.
        query_string (str): a string to match against.

    Returns:
        bool: True if a match is found for `query_string`, False if no match is
            found.
    """
    CONFIDENCE_RATIO = 97
    """int: Minimum confidence ratio to match against."""
    note_content = get_note_text(note)
    ratio = fuzz.token_sort_ratio(
        " ".join([n.lower() for n in note_content]),
        query_string.lower(),
        score_cutoff=CONFIDENCE_RATIO)
    return bool(ratio)


@check_type(JSONModelObject)
def object_locations(archival_object):
    """Finds locations associated with an archival object.

    Args:
        archival_object (JSONModelObject): an ArchivesSpace archival_object.

    Returns:
        list: Locations objects associated with the archival object.
    """
    locations = []
    for instance in archival_object.instances:
        top_container = instance.sub_container.top_container.reify()
        locations += top_container.container_locations
    return locations


@check_type(JSONModelObject)
def format_from_obj(obj, format_string):
    """Generates a human-readable string from an object.

    Args:
        location (dict): an ArchivesSpace object.

    Returns:
        str: a string in the chosen format
    """
    if not format_string:
        raise Exception("No format string provided.")
    else:
        try:
            d = {}
            matches = [i[1] for i in Formatter().parse(format_string) if i[1]]
            for m in matches:
                d.update({m: getattr(obj, m, "")})
            return format_string.format(**d)
        except KeyError as e:
            raise KeyError(
                "The field {} was not found in this object".format(
                    str(e)))


# @check_type(JSONModelObject)
def format_resource_id(resource, separator=":"):
    """Concatenates the four-part ID for a resource record.

    Args:
        resource (JSONModelObject): an ArchivesSpace resource object.
        separator (str): a separator to insert between the id parts. Defaults
            to `:`.

    Returns:
        str: a concatenated four-part ID for the resource record.
    """
    resource_id = []
    for x in range(4):
        try:
            resource_id.append(resource["id_{0}".format(x)])
        except KeyError:
            break
    return separator.join(resource_id)


@check_type(JSONModelObject)
def closest_value(archival_object, key):
    """Finds the closest value matching a key.

    Starts with an archival object, and iterates up through it's ancestors
    until it finds a match for a key that is not empty or null.

    Args:
        archival_object (JSONModelObject): an ArchivesSpace archival_object
        key (str): the key to match against.

    Returns:
        The value of the key, which could be a str, list, or dict
    """
    if getattr(archival_object, key) not in ['', [], {}, None]:
        return getattr(archival_object, key)
    else:
        for ancestor in archival_object.ancestors:
            return closest_value(ancestor, key)


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


# @check_type(JSONModelObject)
def get_expression(date):
    """Returns a date expression for a date object.

    Concatenates start and end dates if no date expression exists.

    Args:
        date (JSONModelObject): an ArchivesSpace date object

    Returns:
        str: a date expression for the date object.
    """
    try:
        expression = date["expression"]
    except KeyError:
        if date.get("end"):
            expression = "{0}-{1}".format(date["begin"], date["end"])
        else:
            expression = date["begin"]
    return expression


# @check_type(JSONModelObject)
def indicates_restriction(rights_statement):
    """Parses a rights statement to determine if it indicates a restriction.

    Args:
        rights_statement (JSONModelObject): an ArchivesSpace rights statement.

    Returns:
        bool: True if rights statement indicates a restriction, False if not.
    """
    def is_expired(date):
        today = datetime.now()
        date = date if date else datetime.strftime("%Y-%m-%d")
        return False if (
            datetime.strptime(date, "%Y-%m-%d") >= today) else True

    if is_expired(rights_statement.get("end_date")):
        return False
    for act in rights_statement.get("acts"):
        if (act.get("restriction") in [
                "disallow", "conditional"] and not is_expired(act.get("end_date"))):
            return True
    return False


# @check_type(JSONModelObject)
def is_restricted(archival_object):
    """Parses an archival object to determine if it is restricted.

    Iterates through notes, looking for a conditions governing access note
    which contains a particular set of strings.
    Also looks for associated rights statements which indicate object may be
    restricted.

    Args:
        archival_object (JSONModelObject): an ArchivesSpace archival_object.

    Returns:
        bool: True if archival object is restricted, False if not.
    """
    query_string = "materials are restricted"
    for note in archival_object['notes']:
        if note['type'] == 'accessrestrict':
            if text_in_note(note, query_string):
                return True
    for rights_statement in archival_object['rights_statements']:
        if indicates_restriction(rights_statement):
            return True
    return False


@check_type(str)
def strip_html_tags(string):
    """Strips HTML tags from a string.

    Args:
        string (str): An input string from which to remove HTML tags.
    """
    tag_match = re.compile('<.*?>')
    cleantext = re.sub(tag_match, '', string)
    return cleantext
