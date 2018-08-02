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
import time
import os
import sys

sys.path.append(os.path.abspath('../NEGF_global'))

from global_write import global_write
from yaml_file_loader import yaml_file_loader


def generate_hamiltonian(input_location, output_location, num_unit):
    ks_matrix = np.array([])
    overlap_matrix = np.array([])

    if os.path.isdir(input_location):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(input_location):
            f.extend(filenames)
            break
        for file in f:
            if file == 'ks_matrix.dat':
                ks_matrix = np.loadtxt(
                                os.path.join(input_location, file),
                                delimiter=' ')
            elif file == 'overlap_matrix.dat':
                overlap_matrix = np.loadtxt(
                                os.path.join(input_location, file),
                                delimiter=' ')
    if ks_matrix.size != 0:
        hn1, h00, hp1, status = matrix_split(ks_matrix, num_unit)
        if status:
            variable_name = ['hn1', 'h00', 'hp1']
            for idx, item in enumerate([hn1, h00, hp1]):
                global_write(output_location,
                             variable_name[idx] + '.dat',
                             num_data=item)
            print('=== Hamiltonian matrix has generated ===')
        else:
            print('Error: Matrix dimension is not divisible by 3')

    if overlap_matrix.size != 0:
        sn1, s00, sp1, status = matrix_split(overlap_matrix, num_unit)
        if status:
            variable_name = ['sn1', 's00', 'sp1']
            for idx, item in enumerate([sn1, s00, sp1]):
                global_write(output_location,
                             variable_name[idx] + '.dat',
                             num_data=item)
            print('=== overlap matrix has generated ===')
        else:
            print('Error: Matrix dimension is not divisible by 3')


def matrix_split(matrix, num_unit):
    matrix_shape = matrix.shape
    if (matrix.shape[0] % num_unit) == 0 and (matrix.shape[1] % num_unit) == 0:
        A = matrix[:int(matrix_shape[0]/num_unit),
                   :int(matrix_shape[0]/num_unit)]
        K = matrix[int(matrix_shape[0]*2/num_unit):,
                   int(matrix_shape[0]*2/num_unit):]
        up_middle_matrix = matrix[:int(matrix_shape[0]/num_unit),
                                  int(matrix_shape[0]/num_unit):int(matrix_shape[0]*2/num_unit)]
        left_matrix = matrix[int(matrix_shape[0]/num_unit):int(matrix_shape[0]*2/num_unit),
                             :int(matrix_shape[0]/num_unit)]
        middle_matrix = matrix[int(matrix_shape[0]/num_unit):int(matrix_shape[0]*2/num_unit),
                               int(matrix_shape[0]/num_unit):int(matrix_shape[0]*2/num_unit)]
        right_matrix = matrix[int(matrix_shape[0]/num_unit):int(matrix_shape[0]*2/num_unit),
                              int(matrix_shape[0]*2/num_unit):]
        low_middle_matrix = matrix[int(matrix_shape[0]*2/num_unit):,
                                   int(matrix_shape[0]/num_unit):int(matrix_shape[0]*2/num_unit)] 

        if np.all(up_middle_matrix == np.matrix.getH(left_matrix)):
            print('B and D+ is the same')
        else:
            print('WARNNING: B and D+ is not the same')

        if np.all(right_matrix == np.matrix.getH(low_middle_matrix)):
            print('F and H+ is the same')
        else:
            print('WARNNING: F and H+ is not the same')

        if np.all(middle_matrix == A) and np.all(middle_matrix == K):
            print('Diagonal elements are the same')
        else:
            print('WARNNING: Diagonal elements are not the same')

        status = True
        return left_matrix, middle_matrix, right_matrix, status
    else:
        left_matrix = np.array([])
        middle_matrix = np.array([])
        right_matrix = np.array([])
        status = False
        return left_matrix, middle_matrix, right_matrix, status


if __name__ == '__main__':
    #get the current location
    location = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))

    input_parameter = yaml_file_loader(location, 'system_parameter.yml')

    generate_hamiltonian(input_parameter['Global']['input_dir'],
                         input_parameter['Global']['output_dir'],
                         int(input_parameter['generate_hamiltonian']['number_of_unit']))

    print('generate_hamiltonian has completed')
