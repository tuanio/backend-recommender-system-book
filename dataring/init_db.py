"""
this file using to create schema from models defining in app/models.py and register numpy data type to psycopg2

Author: Pham Thinh 👋
Contact: github.com/Thinh127
"""

from app import db
import numpy as np
import time
import sys
import os
from psycopg2.extensions import register_adapter, AsIs

start = time.time()

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)

def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

def addapt_numpy_float32(numpy_float32):
    return AsIs(numpy_float32)

def addapt_numpy_int32(numpy_int32):
    return AsIs(numpy_int32)

def addapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))

register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)
register_adapter(np.float32, addapt_numpy_float32)
register_adapter(np.int32, addapt_numpy_int32)
register_adapter(np.ndarray, addapt_numpy_array)

db.drop_all()
db.create_all()

cmds = [
    'transform_data.py'
]

for cmd in cmds:
    sys.stdout.write('Running file: {} \n'.format(cmd))
    os.system('python ' + cmd)
    sys.stdout.write('Done job [{}] \n'.format(cmd))


end = time.time()
sys.stdout.write("init_db.py -> " + str(end - start))