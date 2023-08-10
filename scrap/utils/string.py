def cutoff(v, limit=50, continued="..."):
    """
    Cut off v to max LIMIT characters.  Append CONTINUED to show there is more.  Total length of returned string,
    including the length of CONTINUED, will not exceed LIMIT.

    :param v:  String to cut off if necessary
    :param limit: Max length of the returned string
    :param continued: String to append if v is too long
    :return:
    """
    if len(v) < limit:
        return v
    return f"{v[:limit-len(continued)]}{continued}"
