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
 
import os
import numpy as np
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt


def NEGF_display(e_cap, gs_tra, transmission_tra, output_location):
    fig_location = os.path.join(output_location, 'fig')
    if not os.path.isdir(fig_location):
        os.makedirs(fig_location)

    fig1 = plt.figure(1)
    plt.plot(e_cap, -(1/np.pi)*np.imag(gs_tra), label='Imag')
    plt.xlabel('Energy')
    plt.ylabel('Density of state')
    plt.title('DOS of system')
    plt.legend()
    plt.grid()
    fig1.savefig(os.path.join(fig_location, 'DOS.png'))

    fig2 = plt.figure(2)
    plt.plot(e_cap, transmission_tra)
    plt.xlabel('Energy')
    plt.ylabel('Transmission')
    plt.title('Transmission of system')
    plt.grid()
    fig2.savefig(os.path.join(fig_location, 'Transmission.png'))
