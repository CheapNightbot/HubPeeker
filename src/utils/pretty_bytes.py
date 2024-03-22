"""
It uses base-2 (e.g. kibibyte) and not the base-10 (e.g. kilobyte).

    - 1000 (10³) bytes = 1 kilobyte / 1 kB (base-10)
    - 1024 (2¹⁰) bytes = 1 kibibyte / 1 KiB (base-2)

This one have good and short explanation: https://wiki.ubuntu.com/UnitsPolicy
Also read this: https://web.archive.org/web/20150324153922/https://pacoup.com/2009/05/26/kb-kb-kib-whats-up-with-that/
"""

def pretty_bytes(num: int, suffix='B') -> str:
    """This function takes a number of bytes and returns a string with the size in the most appropriate unit (bytes, kibibytes, mebibytes, etc.). For example, `format_file_size(9697289)` would return `'9.25 MiB'`.

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
