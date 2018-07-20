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

# from src.ao_to_dat_package.load_write_ao import load_ao
# from src.ao_to_dat_package.load_write_ao import write_data

import numpy as np
import argparse
import os
import time

def load_input(location, input_type, target_folder_name):    
    start_time = time.time()
    target_location = os.path.join(location, input_type, target_folder_name)
    total_time = 0.0
    
    if os.path.isdir(target_location):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(target_location):
            f.extend(filenames)
            break
        for file in f:
            if file=='ks_matrix.dat':
                ks_matrix = np.loadtxt(os.path.join(location, input_type, 
                                              target_folder_name, file),
                                              delimiter=',')
            elif file=='overlap_matrix.dat':
                overlap_matrix = np.loadtxt(os.path.join(location, input_type, 
                                              target_folder_name, file), 
                                              delimiter=',')
    if ks_matrix.size != 0:
        hn1, h00, hp1 = matrix_split(ks_matrix)
        variable_name = ['hn1', 'h00', 'hp1']
        for idx, item in enumerate([hn1, h00, hp1]):
            write_data(location, 'output', target_folder_name,
                       variable_name[idx] + '.dat',
                       num_data=item)
        
    if overlap_matrix.size != 0:
        sn1, s00, sp1 = matrix_split(overlap_matrix)
        variable_name = ['sn1', 's00', 'sp1']
        for idx, item in enumerate([sn1, s00, sp1]):
            write_data(location, 'output', target_folder_name,
                       variable_name[idx] + '.dat',
                       num_data=item)


def matrix_split(matrix):
    matrix_shape = matrix.shape
    if matrix.shape[0]%3 == 0 and matrix.shape[1]%3 == 0:
        left_matrix = matrix[int(matrix_shape[0]/3):int(matrix_shape[0]*2/3), 
                             :int(matrix_shape[0]/3)]
        middle_matrix = matrix[int(matrix_shape[0]/3):int(matrix_shape[0]*2/3), 
                             int(matrix_shape[0]/3):int(matrix_shape[0]*2/3)]
        right_matrix = matrix[int(matrix_shape[0]/3):int(matrix_shape[0]*2/3), 
                             int(matrix_shape[0]*2/3):]
        return left_matrix, middle_matrix, right_matrix
    else:
        left_matrix = np.array([])
        middle_matrix = np.array([])
        right_matrix = np.array([])
        write_data(location, 'output', target_folder_name,
                   'output.out',
                   message=['Error: Matrix dimension can not be divisible by 3'])
        return left_matrix, middle_matrix, right_matrix

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

if __name__ == '__main__':
#     start_time = time.time()
    parser = argparse.ArgumentParser(description='Convert ".ao" file into ".dat" file.')
    parser.add_argument("Folder_Name",
                        help="Name of the folder that contains '.ao' file")
    
    args = parser.parse_args()
    
    #get the current location
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    load_input(location, 'input', args.Folder_Name)