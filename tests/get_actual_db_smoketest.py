import os
import shutil

from get_actual_db import get_database_of_lost_places

testpath = os.path.join('.', 'smkoketest')
os.mkdir(testpath)
get_database_of_lost_places(testpath, is_test=True)
if os.path.isfile(os.path.join(testpath, 'item_00050.html')) and os.path.isdir(
        os.path.join(testpath, 'item_00050_files')):
    print('test passed')
else:
    print('test failed')
shutil.rmtree(testpath)
