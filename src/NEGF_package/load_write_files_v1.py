#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018, INT, KIT"
__credits__ = ["Pramit Barua"]
__license__ = "INT, KIT"
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]

'''
This function loads the files in the code. In this project 'input' and 'output' 
folders contain data that need to be loaded in the system. This function is 
capable to handle all sort of input of this project.

input variables of this function:
location: directory address where input and output folder is located in the 
    system
input_type: could be 'input' or 'output'. It defines which folder it should read
target_folder_name: this is the folder name where data is stored. 

program will go into the target folder and read the desire inputs and will
return the content of the input files in numpy array format 

error handling:
* if the target folder does not exist then the program will print an error
'Folder does not exist'
* every target folder should contain 3 files. If the program fail to load 
3 files then it will print 'some files failed to load'
'''


import os
import numpy as np
# import pandas
import time


def load_input(location, input_type, target_folder_name):    
    start_time = time.time()
    target_location = os.path.join(location, input_type, target_folder_name)
    total_time = 0.0
    
    if os.path.isdir(target_location):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(target_location):
            f.extend(filenames)
            break
        for file in f:
            if file=='h00.dat':
                h00 = np.loadtxt(os.path.join(location, input_type, 
                                              target_folder_name, file),
                                              delimiter=',')
            elif file=='hp1.dat':
                hp1 = np.loadtxt(os.path.join(location, input_type, 
                                              target_folder_name, file), 
                                              delimiter=',')
            elif file=='hn1.dat':
                hn1 = np.loadtxt(os.path.join(location, input_type, 
                                              target_folder_name, file), 
                                              delimiter=',')
            elif file=='s00.dat':
                s00 = np.loadtxt(os.path.join(location, input_type, 
                                              target_folder_name, file), 
                                              delimiter=',')
            elif file=='sp1.dat':
                sp1 = np.loadtxt(os.path.join(location, input_type, 
                                              target_folder_name, file), 
                                              delimiter=',')
            elif file=='sn1.dat':
                sn1 = np.loadtxt(os.path.join(location, input_type, 
                                              target_folder_name, file), 
                                              delimiter=',')
            elif file=='T.dat':
                T = np.loadtxt(os.path.join(location, input_type, 
                                            target_folder_name, file), 
                                            delimiter=',').view(complex)
            elif file=='DOS.dat':
                DOS = np.loadtxt(os.path.join(location, input_type, 
                                              target_folder_name, file),
                                              delimiter=',').view(complex)
            elif file=='E.dat':
                E = np.loadtxt(os.path.join(location, input_type, 
                                            target_folder_name, file), 
                                            delimiter=',').view(complex)
        
        end_ts = time.time()
        total_time = end_ts-start_time
        if 'h00' and 'hp1' and 'hn1' in locals():
            if h00.shape == hp1.shape == hn1.shape:
                if 's00' and 'sp1' and 'sn1' in locals():
                    if h00.shape == s00.shape == sp1.shape == sn1.shape:
                        matrix_data = {'h00': h00,
                                       'hp1': hp1,
                                       'hn1': hn1,
                                       's00': s00,
                                       'sp1': sp1,
                                       'sn1': sn1}
                        return matrix_data, total_time   
                    else:
                        print('Matrix dimension mismatched\nCan not proceed further.')
                        write_data(location, 'output', target_folder_name, 
                                   message = ['=== Matrix dimension mismatched. Can not proceed further. ==='])
                        matrix_data = {'h00': np.array([]),
                                       'hp1': np.array([]),
                                       'hn1': np.array([]),
                                       's00': np.array([]),
                                       'sp1': np.array([]),
                                       'sn1': np.array([])}
                        return matrix_data, total_time                                             
                else:
                    matrix_data = {'h00': h00,
                                   'hp1': hp1,
                                   'hn1': hn1,
                                   's00': np.array([]),
                                   'sp1': np.array([]),
                                   'sn1': np.array([])}
                    return matrix_data, total_time
            else:
                print('Matrix dimension mismatched\nCan not proceed further.')
                write_data(location, 'output', target_folder_name, 
                           message = ['=== Matrix dimension mismatched. Can not proceed further. ==='])
                matrix_data = {'h00': np.array([]),
                               'hp1': np.array([]),
                               'hn1': np.array([]),
                               's00': np.array([]),
                               'sp1': np.array([]),
                               'sn1': np.array([])}
                return matrix_data, total_time
        elif 'T' and 'DOS' and 'E' in locals():
            if E.shape == T.shape == DOS.shape:  
                matrix_data = {'E': E,
                               'DOS': DOS,
                               'T': T}
                return matrix_data, total_time
            else:
                print('Input matrix dimension is mismatched\nCan not proceed further.')                
                matrix_data = {'E': np.array([]),
                               'DOS': np.array([]),
                               'T': np.array([])}
                return matrix_data, total_time
        else:
            print('Folder exists. However, files failed to load')
            if input_type == 'input':
                write_data(location, 'output', target_folder_name, 
                           message = ['=== Folder exists. However, files failed to load ==='])
                matrix_data = {'h00': np.array([]),
                               'hp1': np.array([]),
                               'hn1': np.array([]),
                               's00': np.array([]),
                               'sp1': np.array([]),
                               'sn1': np.array([])}
                return matrix_data, total_time
            else:
                matrix_data = {'E': np.array([]),
                               'DOS': np.array([]),
                               'T': np.array([])}
                return matrix_data, total_time
    else:
        print('Folder does not exist')
        if input_type == 'input':
            write_data(location, 'output', target_folder_name, message = ['=== Folder does not exist ==='])
            matrix_data = {'h00': np.array([]),
                           'hp1': np.array([]),
                           'hn1': np.array([]),
                           's00': np.array([]),
                           'sp1': np.array([]),
                           'sn1': np.array([])}
            return matrix_data, total_time
        else:
            matrix_data = {'E': np.array([]),
                           'DOS': np.array([]),
                           'T': np.array([])}
            return matrix_data, total_time
    
def write_data(location, input_type, target_folder_name, **kargs):
    target_location = os.path.join(location, input_type, target_folder_name)
    if not os.path.isdir(target_location):
        os.makedirs(target_location)
        
    if 'E' in kargs:
        np.savetxt(os.path.join(target_location, 'E.dat'), kargs['E'].view(float), delimiter=',')    
    if 'DOS' in kargs:
        np.savetxt(os.path.join(target_location, 'DOS.dat'), kargs['DOS'].view(float), delimiter=',')
    if 'T' in kargs:
        np.savetxt(os.path.join(target_location, 'T.dat'), kargs['T'].view(float), delimiter=',')
    if 'message' in kargs:
        with open(os.path.join(target_location, 'output.out'), "a+") as f:
            for line in kargs['message']:
                f.write(str(line) +"\n")
    
    
if __name__ == '__main__':
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #removing last 2 folders from location variable
    location = location[:location.find('src')]
    h00, hp1, hn1 = load_input(location, 'input', 'zigzag(2,0)_3')
    print(h00, hp1, hn1)