def reduce_list(value, single_item_to_scalar=True):
    """ Takes a value and removes blank values.  Returns a scalar if only one remaining value. """
    if not isinstance(value, list):
        return value
    new_value = [v for v in value if v]
    if len(new_value) > 1:
        return new_value
    elif len(new_value):
        return new_value[0] if single_item_to_scalar else new_value
    else:
        # Nothing in the list.
        return None
