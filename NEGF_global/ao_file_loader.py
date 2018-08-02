#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018, INT, KIT"
__credits__ = ["Pramit Barua"]
__license__ = "INT, KIT"
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


'''
this method takes ao file and return overlap matrix and kohn-sham 
matrix into numpy array

Note: directory should not contain more than one ao file

input argument:
    input_location: ao file directory

output:
    kohn-sham matrix
    overlap matrix
'''

import os
import numpy as np
import sys

sys.path.append(os.path.abspath('../NEGF_global'))

from global_write import global_write


def ao_file_loader(input_location):
    overlap_matrix = []
    ks_matrix = []
    overlap_matrix_visited = False
    ks_matrix_visited = False
    overlap_matrix_write = False
    ks_matrix_write = False

    if os.path.isdir(input_location):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(input_location):
            f.extend(filenames)
            break

        ao_visited = False
        for file in f:
            if '.ao' in file:
                print('=== ".ao" file found ===')
                ao_visited = True
                with open(os.path.join(input_location, file), "r") as raw_data:
                    for line in raw_data:
                        if line == ' OVERLAP MATRIX\n':
                            if not overlap_matrix_visited:
                                overlap_matrix_visited = True
                                overlap_matrix_write = True
                                ks_matrix_write = False
                            elif ks_matrix_visited:
                                break
                        elif line == ' KOHN-SHAM MATRIX\n':
                            if not ks_matrix_visited:
                                ks_matrix_visited = True
                                ks_matrix_write = True
                                overlap_matrix_write = False
                            elif overlap_matrix_visited:
                                break

                        if overlap_matrix_visited and overlap_matrix_write:
                            if line == '\n':
                                pass
                            else:
                                line = line.split()
                                if len(line) > 4:
                                    data_value = []
                                    for item in line[4:]:
                                        data_value.append(float(item))
                                    try:
                                        overlap_matrix[int(line[0])-1].extend(data_value)
                                    except IndexError:
                                        overlap_matrix.append(data_value)

                        elif ks_matrix_visited and ks_matrix_write:
                            if line == '\n':
                                pass
                            else:
                                line = line.split()
                                if len(line) > 4:
                                    data_value = []
                                    for item in line[4:]:
                                        data_value.append(float(item)*27.2114)
                                    try:
                                        ks_matrix[int(line[0])-1].extend(data_value)
                                    except IndexError:
                                        ks_matrix.append(data_value)
                break

        if not ao_visited:
            print('ao file not found')
    else:
        print('Directory does not exist')

    return np.array(ks_matrix), np.array(overlap_matrix)