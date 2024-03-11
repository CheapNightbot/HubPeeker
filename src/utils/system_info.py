import platform
import logging

from . import json

def get_system_info():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['architecture']=[platform.machine(), platform.architecture()[0]]

        return json.dumps(info)
    except Exception as e:
        logging.exception(e)
