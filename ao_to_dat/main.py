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

from src.ao_to_dat_package.load_write_ao import load_ao
from src.ao_to_dat_package.load_write_ao import write_data

import pandas as pd
import argparse
import os


if __name__ == '__main__':
#     start_time = time.time()
    parser = argparse.ArgumentParser(description='Convert ".ao" file into ".dat" file.')
    parser.add_argument("Folder_Name",
                        help="Name of the folder that contains '.ao' file")
    
    args = parser.parse_args()
    
    #get the current location
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    load_ao(location, 'input', args.Folder_Name)