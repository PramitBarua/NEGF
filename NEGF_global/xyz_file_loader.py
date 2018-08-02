#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018, INT, KIT"
__credits__ = ["Pramit Barua"]
__license__ = "INT, KIT"
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


r'''
this method returns atom name and coordinate of atoms from xyz file
atom name is in list and coordinate is in numpy array
input argument:
    file_name:
        it contains the directory address of the xyz file, including the file name
        example: C:\Users\Desktop\nt-4-0-3.xyz
 
output/return:
    atom name
    x, y and z coordinates
'''

import numpy as np


def xyz_file_loader(file_name):
    atoms = []
    coordinates = []

    xyz = open(file_name)
    n_atoms = int(xyz.readline())
    title = xyz.readline()
    for line in xyz:
        try:
            atom, x, y, z = line.split()
            atoms.append(atom)
            coordinates.append([float(x), float(y), float(z)])
        except ValueError:
            pass
    xyz.close()

    if n_atoms != len(coordinates):
        atoms = []
        coordinates = []

    return atoms, np.array(coordinates)


if __name__ == '__main__':
    xyz_file_loader(r'C:\Users\PRAMIT\Documents\MEGA\Master thesis\pramit\python code\related to thesis\zz_tube_xyz_generator\graphene_16_3.xyz')
