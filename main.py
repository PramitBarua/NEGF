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

def system_gs(item_E, hc, sh, sigma_l, sigma_r):
    start_time = time.time()
    gs = np.linalg.inv(item_E*np.eye(len(sh))@sh - hc - sigma_l - sigma_r)
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
                        help="(y/n) for keep track of the execution time")
    
    args = parser.parse_args()
    
    time_list = []
    time_list.append('\n=== Time ===')
    #get the current location
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    write_data(location, 'output', args.Folder_Name, message=['=== NEGF starts ==='])
    
    data_matrix, time_took = load_input(location, 'input', args.Folder_Name)
    time_list.append('time took to load file: %f' % (time_took))
    
    if data_matrix['h00'].size != 0 and data_matrix['s00'].size != 0:
        hc = data_matrix['h00']
        hctl = data_matrix['hn1']
        hctr = data_matrix['hp1']
        s00 = data_matrix['s00']
        sctl = data_matrix['sn1']
        sctr = data_matrix['sp1']
    elif data_matrix['h00'].size != 0 and data_matrix['s00'].size == 0:
        hc = data_matrix['h00']
        hctl = data_matrix['hn1']
        hctr = data_matrix['hp1']
        s00 = np.eye(len(hc))
        sctl = np.zeros(hc.shape)
        sctr = np.zeros(hc.shape) 
        
    if 'hc' in locals():    
        write_data(location, 'output', args.Folder_Name, message=['=== Matrix has been loaded ==='])
        e_cap = np.linspace(-10, 10, 1000)
        e_cap = e_cap+1j*0.001    
         
        sigma_l_trace = np.empty(len(e_cap), dtype=complex)
        gs = np.empty(len(e_cap), dtype=object)
        gs_tra = np.empty(len(e_cap), dtype=complex)
        transmission_tra = np.empty(len(e_cap), dtype=complex)
          
        time_g00_l = 0
        time_g00_r = 0
        time_gs = 0
         
        for idx1, item_E in enumerate(e_cap):
            g00_l, time_took  = self_energy(item_E, hc, hctl, s00, sctl)
            sigma_l = (item_E*sctl - hctl) @ g00_l @ np.matrix.getH(item_E*sctl - hctl)
            time_g00_l = time_g00_l + time_took
             
            g00_r, time_took  = self_energy(item_E, hc, hctr, s00, sctr)
            sigma_r = (item_E*sctr - hctr) @ g00_r @ np.matrix.getH(item_E*sctr - hctr)
            time_g00_r = time_g00_r + time_took
                         
            gs[idx1], time_took = system_gs(item_E, hc, s00, sigma_l, sigma_r)
            time_gs = time_gs + time_took
            gs_tra[idx1] = np.trace(gs[idx1]@s00)
#             gs_tra[idx1] = np.trace(1j*(gs[idx1] - np.matrix.getH(gs[idx1])))
    #            
            gamma_l = 1j*(sigma_l-np.matrix.getH(sigma_l))
            gamma_r = 1j*(sigma_r-np.matrix.getH(sigma_r))
    #            
            transmission = gamma_l @ gs[idx1] @ gamma_r @ np.matrix.getH(gs[idx1])
            transmission_tra[idx1] = np.trace(transmission)
         
        end_ts = time.time()
        time_took = end_ts-start_time  
        time_g00_l = time_g00_l/len(e_cap)
        time_g00_r = time_g00_r/len(e_cap)
        time_gs = time_g00_l/len(e_cap)
         
        time_list.append('average time to calculate g00_l %f' % (time_g00_l))
        time_list.append('average time to calculate g00_r %f' % (time_g00_r))
        time_list.append('average time to calculate gs %f' % (time_gs))
        time_list.append('time took for total calculation %f \n' % (time_took)) 
        
        write_data(location, 'output', args.Folder_Name, message=['=== NEGF has completed ==='])
        
        if args.timing == 'y' or args.timing == 'Y':
            write_data(location, 'output', args.Folder_Name, message=['=== Saving Data ==='])
            write_data(location, 'output', args.Folder_Name, E = e_cap, DOS = gs_tra, T = transmission_tra, message=time_list)
        else:
            write_data(location, 'output', args.Folder_Name, message=['=== Saving Data ==='])
            write_data(location, 'output', args.Folder_Name, E = e_cap, DOS = gs_tra, T = transmission_tra)
            
        write_data(location, 'output', args.Folder_Name, message=['=== Display ==='])
        display_data(e_cap, gs_tra, transmission_tra, args.Folder_Name, args.plot)
        