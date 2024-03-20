def format_file_size(num: int, suffix='B'):
    """This function takes a number of bytes and returns a string with the size in the most appropriate unit (bytes, kilobytes, megabytes, etc.). For example, `format_file_size(9697289)` would return `'9.2 MiB'`.

    Args:
        - `num` (int): The file size in bytes.
        - `suffix` (str, optional): The unit of the file size. Defaults to 'B'.

    Returns:
        - `str` : Returns a string representing `num` in  human-readable format (unit), rounded to two decimal place.
    """
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)
