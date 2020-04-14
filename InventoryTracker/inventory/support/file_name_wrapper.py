import time
from uuid import uuid4
import os

def PathAndRename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        TimeStr = time.strftime('%y-%j')
        if instance.pk:
            filename = '{}-{}.{}'.format(instance.pk, uuid4().hex, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        Temp = time.strftime(path)
        return os.path.join(Temp, filename)
    return wrapper
