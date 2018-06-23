#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018, INT, KIT"
__credits__ = ["Pramit Barua"]
__license__ = "INT, KIT"
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]

'''
This code is for one electrode is 2D and another electrode is 1D. The quantum 
system is 3 atom connected in a triangular shape
'''

from NEGF_package.load_input_v1 import load_input
# from yaml_loader import CSV_loader
# from self_energy_v2 import self_energy

import numpy as np
import os
import matplotlib.pyplot as plt
import argparse
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-FN", "--Folder_Name",
                        help="Name of the folder that contains input files ")
                        
#     __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    load_input('zigzag(2,0)_3')
    '''
    call the function that can read the .dat files and return in numpy
    in function it has to identity the folder, read the file with appropriate 
    name(check the name of the file and assign it to appropriate variable)
    '''
    args = parser.parse_args()
    print(args.Folder_Name)
    data = yaml_loader(args.File_Name)
    
#     t0 = float(data['t0'])
#     eta = float(data['eta'])
    hc = CSV_loader(data['hc'])
    hctl = CSV_loader(data['hctl'])
    hctr = CSV_loader(data['hctr'])
    
#     eig_val, eig_vec = np.linalg.eig(hc)
#     print('eigen value of the quantum system : '+'\n'+ str(eig_val))
    
    e_cap = np.linspace(-4*t0, 4*t0, 1000)
    e_cap = e_cap+1j*eta
    
    g00_l = np.empty(len(e_cap), dtype=complex)
    g00_r = np.empty(len(e_cap), dtype=complex)
    sigma_l_trace = np.empty(len(e_cap), dtype=complex)
    gs = np.empty(len(e_cap), dtype=object)
    gs_tra = np.empty(len(e_cap), dtype=complex)
    transmission_tra = np.empty(len(e_cap), dtype=complex)
     
    for idx1, item_E in enumerate(e_cap):
        sigma_l, g00_l[idx1] = self_energy(item_E, hc, hctl)
        sigma_r, g00_r[idx1] = self_energy(item_E, hc, hctr)
                        
        gs[idx1] = np.linalg.inv(item_E*np.eye(len(hc)) - hc - sigma_l - sigma_r)
        gs_tra[idx1] = np.trace(gs[idx1])
#            
        gamma_l = 1j*(sigma_l-np.matrix.getH(sigma_l))
        gamma_r = 1j*(sigma_r-np.matrix.getH(sigma_r))
#            
        transmission = gamma_l @ gs[idx1] @ gamma_r @ np.matrix.getH(gs[idx1])
        transmission_tra[idx1] = np.trace(transmission)
     
#     plt.figure(1)
# #     line2 = plt.plot(e_cap, g00_tra.real, '-.', label='Real')
#     line3 = plt.plot(e_cap, np.imag(sigma_l_trace), label='Imag')
#     plt.xlabel('Energy')
#     plt.ylabel('Density of state')
#     plt.legend()
#     plt.grid()
    
    
    plt.figure(2)
    line3 = plt.plot(e_cap, -(1/np.pi)*np.imag(gs_tra), label='Imag')
    plt.xlabel('Energy')
    plt.ylabel('Density of state')
    plt.title('DOS of system')
    plt.legend()
    plt.grid()
         
    plt.figure(3)
    line3 = plt.plot(e_cap, transmission_tra)
    plt.xlabel('Energy')
    plt.ylabel('Transmission')
    plt.title('Transmission of system')
    plt.grid()
#      
    plt.show()