#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018, INT, KIT"
__credits__ = ["Pramit Barua"]
__license__ = "INT, KIT"
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]

import numpy as np

def self_energy(energy, h, t0_matrix):
    es = energy*np.eye(len(h))-h
    
    e = energy*np.eye(len(h))-h
    a = -t0_matrix
    b = -np.matrix.getH(t0_matrix)
    
    
    
    while((np.linalg.norm(abs(a), ord='fro') + np.linalg.norm(abs(b), ord='fro')) > 0.001):
        g = np.linalg.inv(e)
        bga = b @ g @ a
        agb = a @ g @ b
        e = e - bga - agb
        es = es - agb
        
        a = -a @ g @ a
        b = -b @ g @ b
    
    g = np.linalg.inv(es)
    return t0_matrix @ g @ np.matrix.getH(t0_matrix), np.trace(g)    
#     return g, np.trace(g) 
        