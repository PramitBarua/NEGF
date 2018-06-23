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

from src.NEGF_package.load_write_files_v1 import load_input
from src.NEGF_package.load_write_files_v1 import write_data
from src.NEGF_package.self_energy_v2 import self_energy
from src.NEGF_package.display_data_v1 import display_data


import numpy as np
import os
import argparse
import time

def system_gs(item_E, hc, sigma_l, sigma_r):
    start_time = time.time()
    gs = np.linalg.inv(item_E*np.eye(len(hc)) - hc - sigma_l - sigma_r)
    end_ts = time.time()
    total_time = end_ts-start_time
    return gs, total_time
    
if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser(description='Calculate and display DOS '+
                                     'and transmission of the quantum system.')
    parser.add_argument("Folder_Name",
                        help="Name of the folder that contains input files")
    parser.add_argument("-p","--plot", default = 'y',
                        help="(y/n) for plotting the data")
    parser.add_argument("-t","--timing", default = 'y',
                        help="(y/n) for keep track of the exicution time")
    
    args = parser.parse_args()
    time_list = []
    #get the current location
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    hc, hctr, hctl, time_took = load_input(location, 'input', args.Folder_Name)
    time_list.append('time took to load file: %f' % (time_took))
    
    
    e_cap = np.linspace(-2, 2, 1000)
    e_cap = e_cap+1j*0.001
    
    g00_l = np.empty(len(e_cap), dtype=complex)
    g00_r = np.empty(len(e_cap), dtype=complex)
    sigma_l_trace = np.empty(len(e_cap), dtype=complex)
    gs = np.empty(len(e_cap), dtype=object)
    gs_tra = np.empty(len(e_cap), dtype=complex)
    transmission_tra = np.empty(len(e_cap), dtype=complex)
     
    for idx1, item_E in enumerate(e_cap):
        sigma_l, g00_l[idx1], time_took  = self_energy(item_E, hc, hctl)
        time_list.append('time took to calculate sigma_l: %f' % (time_took))
        sigma_r, g00_r[idx1], time_took = self_energy(item_E, hc, hctr)
        time_list.append('time took to calculate sigma_r: %f' % (time_took))
                        
#         gs[idx1] = np.linalg.inv(item_E*np.eye(len(hc)) - hc - sigma_l - sigma_r)
        gs[idx1], time_took = system_gs(item_E, hc, sigma_l, sigma_r)
        time_list.append('time took to calculate system_gs: %f' % (time_took))
        gs_tra[idx1] = np.trace(gs[idx1])
#            
        gamma_l = 1j*(sigma_l-np.matrix.getH(sigma_l))
        gamma_r = 1j*(sigma_r-np.matrix.getH(sigma_r))
#            
        transmission = gamma_l @ gs[idx1] @ gamma_r @ np.matrix.getH(gs[idx1])
        transmission_tra[idx1] = np.trace(transmission)
    
    end_ts = time.time()
    time_took = end_ts-start_time   
    time_list.append('time took for total calculation %f' % (time_took)) 
    
    if args.timing == 'y' or args.timing == 'Y':
        write_data(location, 'output', args.Folder_Name, E = e_cap, DOS = gs_tra, T = transmission_tra, time=time_list)
    else:
        write_data(location, 'output', args.Folder_Name, E = e_cap, DOS = gs_tra, T = transmission_tra)
        
    
    display_data(e_cap, gs_tra, transmission_tra, args.Folder_Name, args.plot)
    