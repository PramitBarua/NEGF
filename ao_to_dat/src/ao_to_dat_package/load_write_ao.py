#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018, INT, KIT"
__credits__ = ["Pramit Barua"]
__license__ = "INT, KIT"
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


import os
import numpy as np
import time


def load_ao(location, input_type, target_folder_name):
    start_time = time.time()
    target_location = os.path.join(location, input_type, target_folder_name)
    total_time = 0.0

    overlap_matrix = []
    ks_matrix = []
    overlap_matrix_visited = False
    ks_matrix_visited = False
    overlap_matrix_write = False
    ks_matrix_write = False

    if os.path.isdir(target_location):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(target_location):
            f.extend(filenames)
            break

        for file in f:
            if '.ao' in file:
                write_data(location, 'output', target_folder_name,
                           'output.out',
                           message=['=== ".ao" file found ==='])
                with open(os.path.join(target_location, file), "r") as raw_data:
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
                                        data_value.append(float(item))
                                    try:
                                        ks_matrix[int(line[0])-1].extend(data_value)
                                    except IndexError:
                                        ks_matrix.append(data_value)
                break
        if ks_matrix:
            write_data(location, 'output', target_folder_name,
                       'output.out',
                       message=['=== writing ks_matrix ==='])
            write_data(location, 'output', target_folder_name,
                       'ks_matrix.dat', num_data=np.array(ks_matrix))

        if overlap_matrix:
            write_data(location, 'output', target_folder_name,
                       'output.out',
                       message=['=== writing overlap_matrix ==='])
            write_data(location, 'output', target_folder_name,
                       'overlap_matrix.dat', num_data=np.array(overlap_matrix))
        end_ts = time.time()
        total_time = end_ts-start_time
        write_data(location, 'output', target_folder_name,
                   'output.out',
                   message=['Time took: ' + str(total_time)])


def write_data(location, input_type, target_folder_name, file_name, **kargs):

    target_location = os.path.join(location, input_type, target_folder_name)
    if not os.path.isdir(target_location):
        os.makedirs(target_location)

    if 'num_data' in kargs:
        np.savetxt(os.path.join(target_location, file_name),
                   kargs['num_data'].view(float), delimiter=',')

    elif 'message' in kargs:
        with open(os.path.join(target_location, file_name), "a+") as f:
            for line in kargs['message']:
                f.write(str(line) + "\n")
