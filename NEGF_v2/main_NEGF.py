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

import numpy as np
import os
import sys
import time

sys.path.append(os.path.abspath('../NEGF_global'))

from global_write import global_write
from yaml_file_loader import yaml_file_loader

from NEGF_package.NEGF_display import NEGF_display
from NEGF_package.self_energy_v2 import self_energy


def system_gs(item_E, hc, sh, sigma_l, sigma_r):
    start_time = time.time()
    gs = np.linalg.inv(item_E*np.eye(len(sh))@sh - hc - sigma_l - sigma_r)
    end_ts = time.time()
    total_time = end_ts-start_time
    return gs, total_time


def load_dat(location):
    return np.loadtxt(location, delimiter=' ')


if __name__ == '__main__':
    print('=== NEGF starts ===')
    status = True
    start_time = time.time()
    location = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))

    input_parameter = yaml_file_loader(location, 'system_parameter.yml')

    time_list = ['=== Time ===']
    try:
        hc = load_dat(os.path.join(input_parameter['Global']['input_dir'],
                                   'h00.dat'))
        hctl = load_dat(os.path.join(input_parameter['Global']['input_dir'],
                                     'hn1.dat'))
        hctr = load_dat(os.path.join(input_parameter['Global']['input_dir'],
                                     'hp1.dat'))
    except OSError:
        print('!!! Error: Hamiltonian file does not exist !!!')
        status = False
    else:
        try:
            s00 = load_dat(os.path.join(input_parameter['Global']['input_dir'],
                                        's00.dat'))
        except OSError:
            s00 = np.eye(len(hc))

        try:
            sctl = load_dat(os.path.join(input_parameter['Global']['input_dir'],
                                         'sn1.dat'))
        except OSError:
            sctl = np.zeros(hc.shape)

        try:
            sctr = load_dat(os.path.join(input_parameter['Global']['input_dir'],
                                         'sp1.dat'))
        except OSError:
            sctr = np.zeros(hc.shape)

        print('=== Matrices are loaded ===')
        if hc.size == hctl.size == hctr.size == s00.size == sctl.size == sctr.size:
            status = True
            print('=== Matrices are same size ===')
        else:
            status = False
            print('!!! Error: Matrices are not the same size !!!')

    if status:
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
            g00_l, time_took = self_energy(item_E, hc, hctl, s00, sctl)
            sigma_l = (item_E*sctl - hctl) @ g00_l @ np.matrix.getH(item_E*sctl - hctl)
            time_g00_l = time_g00_l + time_took

            g00_r, time_took = self_energy(item_E, hc, hctr, s00, sctr)
            sigma_r = (item_E*sctr - hctr) @ g00_r @ np.matrix.getH(item_E*sctr - hctr)
            time_g00_r = time_g00_r + time_took

            gs[idx1], time_took = system_gs(item_E, hc, s00, sigma_l, sigma_r)
            time_gs = time_gs + time_took
            gs_tra[idx1] = np.trace(gs[idx1]@s00)

            gamma_l = 1j*(sigma_l-np.matrix.getH(sigma_l))
            gamma_r = 1j*(sigma_r-np.matrix.getH(sigma_r))

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

        print('=== NEGF calculation has completed ===')

        print('=== Saving E.dat file ===')
        global_write(input_parameter['Global']['output_dir'],
                     'E.dat',
                     num_data=e_cap)

        print('=== Saving DOS.dat file ===')
        global_write(input_parameter['Global']['output_dir'],
                     'DOS.dat',
                     num_data=gs_tra)

        print('=== Saving T.dat file ===')
        global_write(input_parameter['Global']['output_dir'],
                     'T.dat',
                     num_data=transmission_tra)

        if input_parameter['NEGF_input']['time'] == 'y':
            for line in time_list:
                print(line)

        if input_parameter['NEGF_input']['plot'] == 'y':
            NEGF_display(e_cap,
                         gs_tra,
                         transmission_tra,
                         input_parameter['Global']['output_dir'])
