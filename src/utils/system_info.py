import logging
import platform

from . import json


def get_system_info():
    """Return system information as a dictionary."""
    try:
        info={}
        info['platform']=platform.system().lower()
        info['architecture']=[platform.machine().lower(), platform.architecture()[0].lower()]

        """
        As 'AMD64', 'x64' and 'x86_64' all refer to the same '64-bit' architecture CPU 
        and the `platform` module returns different one of them on different OS, 
        I was able to get 'x64bit' and 'AMD64' (combining Linux & Windows), but it 
        wasn't returning 'x86_64' and some of the asset names on GitHub release were 
        using 'x86_64' and some 'AMD64'. So, for work-around (as mentioned already, 
        they all means '64-bit CPU'), we just check if `platform` module returns 
        'architecture' containing '64' and assume it's a '64-bit CPU' and manual 
        append 'x86_64' to 'architecture' key. ヾ(￣▽￣) Bye~Bye~
        """
        for arch in info.get('architecture'):
            if "64" in arch:
                if arch != "x86_64":
                    info['architecture'].append("x86_64")
                else:
                    info['architecture'].append("amd64")
                break

        return json.dumps(info)
    except Exception as e:
        logging.exception(e)
