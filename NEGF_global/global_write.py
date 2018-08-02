#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018, INT, KIT"
__credits__ = ["Pramit Barua"]
__license__ = "INT, KIT"
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]

''' read me:
This is the global function to write data into file
ideally this function should handle any sort of data
this function can write any type of file (.dat, .out, .xyz)

Data type can be:
    1. purely numeric
    2. purely string

arguments:
    location: where data file will be saved (directory address)
    file_name: name of the file where data will be stored
    *kargs: it contains 2 types of key
        num_data: if data is purely numerical (numpy array)
        message: if data is string (wrapped in a list)
            message is in append mode which means if the file exists
            then program will append data instead of over writing.

note: in any situation if data contains number as well as
string then convert data into string and wrapped each line
in a list. However, this wrapping should be done outside of
this function
'''

import os
import numpy as np


def global_write(location, file_name, **kargs):

#     target_location = os.path.join(location, input_type, target_folder_name)
    if not os.path.isdir(location):
        os.makedirs(location)

    if 'num_data' in kargs:
        np.savetxt(os.path.join(location, file_name),
                   kargs['num_data'].view(float), delimiter=' ')

    if 'message' in kargs:
        with open(os.path.join(location, file_name), "a+") as f:
            for line in kargs['message']:
                f.write(str(line) + "\n")
