import logging
import platform

from . import json


def get_system_info():
    """Return system information as a dictionary."""
    try:
        info={}
        info['platform']=platform.system().lower()
        info['architecture']=[platform.machine().lower(), platform.architecture()[0].lower()]

        for arch in info.get('architecture'):
            if "64" in arch:
                info['architecture'].append("x86_64")
                break

        return json.dumps(info)
    except Exception as e:
        logging.exception(e)
