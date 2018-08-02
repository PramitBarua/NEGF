#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018, INT, KIT"
__credits__ = ["Pramit Barua"]
__license__ = "INT, KIT"
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]

'''

'''

import os
import sys
import numpy as np
import time

sys.path.append(os.path.abspath('../NEGF_global'))

from global_write import global_write
from yaml_file_loader import yaml_file_loader
from ao_file_loader import ao_file_loader

if __name__ == '__main__':
    # get the current location
    location = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))

    input_parameter = yaml_file_loader(location, 'system_parameter.yml')

    start_time = time.time()
    ks_matrix, overlap_matrix = ao_file_loader(input_parameter['Global']['input_dir'])
    end_ts = time.time()
    total_time = end_ts-start_time
    print('Time took to read ao: ' + str(total_time))

    start_time = time.time()
    if ks_matrix.size != 0:
        print('=== writing ks_matrix ===')
        global_write(input_parameter['Global']['output_dir'],
                     'ks_matrix.dat',
                     num_data=np.array(ks_matrix))

    if overlap_matrix.size != 0:
        print('=== writing overlap_matrix ===')
        global_write(input_parameter['Global']['output_dir'],
                     'overlap_matrix.dat',
                     num_data=np.array(overlap_matrix))
    end_ts = time.time()
    total_time = end_ts-start_time
    print('Time took to write dat: ' + str(total_time))

    print('ao_to_dat.py has completed')
