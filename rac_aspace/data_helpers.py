def get_note_text(note):
    """Returns note content as a list."""
    def parse_subnote(subnote):
        """Returns content in subnotes"""
        if subnote.jsonmodel_type in [
                'note_orderedlist', 'note_definedlist', 'note_index',
                'note_chronology']:
            return subnote.items
        elif subnote.jsonmodel_type == 'note_bibliography':
            data = []
            data.append(subnote.content)
            data.append(subnote.items)
            return data
        else:
            return subnote.content if isinstance(
                subnote.content, list) else [subnote.content]

    if note.jsonmodel_type == "note_singlepart":
        return note.source.content.strip("]['").split(', ')
    elif note.jsonmodel_type == "note_index":
        return note.source.items.strip("]['").split(', ')
    else:
        return (parse_subnote(sn) for sn in note.subnotes)


def notes_by_type(notes_array, note_type):
    """Returns notes in a notes array which match a note type."""
    return [note for note in notes_array if note.jsonmodel_type == note_type]


def dates_by_type(dates_array, date_type):
    "Returns a list of dates which match a date type."
    return [date for date in dates_array if date.jsonmodel_type == date_type]


def get_locations(archival_object):
    """
    Returns a list of locations objects associated with an
    archival object.
    """
    locations = []
    for instance in archival_object.instances:
        locations.append(instance.top_container.location)
    return locations


def format_location(location):
    """Return a human-readable string for a location."""
    pass
# QUESTION: pass a format string
# QUESTION: is this a more generalizable function?
# grab fields from location
# format string "{} {}, {}-{}"
# return format string


def format_container(top_container):
    """
    Returns a human-readable concatenation of top container type
    and indicator.
    """
    return "{0} {1}".format(top_container.container_type,
                            top_container.indicator)


def format_resource_id(resource, separator=":"):
    """
    Returns the four-part ID for a resource record. Accepts an optional
    separator argument, which is set to ":" by default
    """
    resource_id = []
    for x in range(3):
        try:
            resource_id.append(getattr(resource, "id_{}".format(x)))
        except AttributeError:
            break
    return separator.join(resource_id)


def closest_value(archival_object, key):
    """
    Returns the closest matching for a key, iterating up through an object's
    ancestors until it finds a match.
    """
    if getattr(archival_object, key) not in ['', [], {}, None]:
        return archival_object.key
    else:
        for ancestor in archival_object.ancestors:
            return closest_value(ancestor, key)


def get_orphans(object_list, null_attribute):
    """
    Generator function which returns objects that do not have a value in a
    specified field.
    """
    for obj in object_list:
        if getattr(obj, null_attribute) in ['', [], {}, None]:
            yield obj


def expression(date):
    """Always returns a date expression for a date object."""
    if date.expression:
        return date.expression
    if date.date_end:
        return "{} - {}".format(date.date_start, date.date_end)
    else:
        return date.date_start


def associated_objects(top_container):
    """Return all the archival objects associated with a top container."""
    pass
# probably have to do some SOLR stuff
#


def is_restricted(archival_object):
    """
    Return a boolean which indicates if an object is restricted.

    Iterates through notes, looking for a conditions governing access note
    which contains a particular set of strings.
    Also looks for associated rights statements which indicate object may be
    restricted.
    """
    pass
# loop through notes, looking for conditions govering access
# look for specific text in matches
# return True
# return False


def get_user_input(prompt):
    """Allows users to input data."""
    print(prompt)
    return raw_input()


def get_config():
    """Sets up configuration values necessary for ASpace."""
    pass
    # look for file
    # look for env variables
