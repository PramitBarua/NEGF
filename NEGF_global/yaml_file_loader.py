#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018, INT, KIT"
__credits__ = ["Pramit Barua"]
__license__ = "INT, KIT"
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]

'''
this method load yaml file.

argument for this method:
    location: directory of ymal file
    name_yaml: name of the yaml file

general format of yaml file:
    compulsory input
        left_graphene_sheet_name:
            contain the directory address of input file (left part)
        left_tube_name:
            contain the directory address of input file (left part)

    optional inputs:
        middle_tube_name:
            name of the xyz file that contian cartesian coordinates
            of each atom of tube (middle part)
        right_graphene_sheet_name:
            name of the xyz file that contain cartesian coordinates
            of each atom of graphene sheet (right part)
        right_tube_name:
            name of the xyz file that contian cartesian coordinates
            of each atom of tube (right part)
'''

import os
import yaml


def yaml_file_loader(location, name_yaml):
    if os.path.isdir(location):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(location):
            f.extend(filenames)
            break

#         ao_visited = False
        for file in f:
            if file == name_yaml:
                with open(os.path.join(location, file), "r") as raw_data:
                    data = yaml.load(raw_data)
                return data['Input']
