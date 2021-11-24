import time

start_time = time.perf_counter()

from dataring.init_db import *
from dataring.transform_data import *

end_time = time.perf_counter()

print(f"It's cost {end_time - start_time} seconds to run this pipeline!")