#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018, INT, KIT"
__credits__ = ["Pramit Barua"]
__license__ = "INT, KIT"
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]

'''
this function displays and saves the density of state(DOS) and transmission of 
a system input of the function is energy, DOS and Transmission data 
'''

from src.NEGF_package.load_write_files_v1 import load_input 
import os
import numpy as np
import matplotlib.pyplot as plt

def display_data(e_cap, gs_tra, transmission_tra, target_folder_name, show_plot):    
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #removing last 2 folders from location variable
    location = location[:location.find('src')]
    target_location = os.path.join(location, 'output', target_folder_name, 'fig')
    if not os.path.isdir(target_location):
        os.makedirs(target_location)
    
#     plt.figure(1)
# #     line2 = plt.plot(e_cap, g00_tra.real, '-.', label='Real')
#     line3 = plt.plot(e_cap, np.imag(sigma_l_trace), label='Imag')
#     plt.xlabel('Energy')
#     plt.ylabel('Density of state')
#     plt.legend()
#     plt.grid()

    fig1 = plt.figure(1)
    plt.plot(e_cap, -(1/np.pi)*np.imag(gs_tra), label='Imag')
    plt.xlabel('Energy')
    plt.ylabel('Density of state')
    plt.title('DOS of system')
    plt.legend()
    plt.grid()
    fig1.savefig(os.path.join(target_location, 'DOS.png'))
         
    fig2 = plt.figure(2)
    plt.plot(e_cap, transmission_tra)
    plt.xlabel('Energy')
    plt.ylabel('Transmission')
    plt.title('Transmission of system')
    plt.grid()
    fig2.savefig(os.path.join(target_location, 'Transmission.png'))
 
    if show_plot == 'y' or show_plot == 'Y':
        plt.show()
    
if __name__ == '__main__':
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #removing last 2 folders from location variable
    location = location[:location.find('src')] 
    E, DOS, T, time_took= load_input(location, 'output', 'zigzag(2,0)_1', 'test')
    if E.size != 0:
        display_data(E, DOS, T, 'random_test', 'y')
    
    