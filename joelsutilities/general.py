import json
import jsonpickle


def prettified_members(o, indent=4):
    """deep object with all members printed for dicts/classes"""

    # pickle into json (string) form
    pickled = jsonpickle.encode(o)

    # load back into object form (with subtrees for all object members)
    json_object = json.loads(pickled)

    # use json to convert to string but this time with indents
    return json.dumps(json_object, indent=indent)


def closest_value(array, value, return_index=False, round_down=False, round_up=False):
    """# get closest value in numpy array, specify return_index=True to return index instead of value"""

    # get index in reversed array of smallest distance to value
    index = abs(array - value).argmin()

    # round down if necessary
    if round_down and index > 0 and array[index] > value:
        index -= 1

    # round up if necessary
    if round_up and index < (len(array) - 1) and array[index] < value:
        index += 1

    if return_index:
        return int(index)  # return as regular integer
    else:
        # return value from reversed array
        return array[index]


def constructor_verify(value, object_type) -> bool:
    """Returns True if can create object from type"""
    try:
        object_type(value)
        return True
    except (ValueError, TypeError) as e:
        return False


