import logging
import platform

from . import json


def get_system_info():
    """Return system information as a dictionary."""
    try:
        info={}
        info['platform']=platform.system().lower()
        info['platform-release']=platform.release().lower()
        info['architecture']=[platform.machine().lower(), platform.architecture()[0].lower()]

        return json.dumps(info)
    except Exception as e:
        logging.exception(e)
