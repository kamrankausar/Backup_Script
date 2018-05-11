#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 17:50:12 2018

@author: kamran
"""
# importing Built-in Module
import os



#Checking for pip module 
try:
  import pip
except ImportError:
  print("Trying to Install required module: pip\n")
  # import the os package to install pip module if not install
  os.system('python -m pip install pip')
  import pip

#Suit to install modules
def install_module(module):
    pip.main(['install', module])

# Checking each library and install if not 
# For Pandas 
try:
    import pandas as pd
except ImportError:
    print("Trying to install required module: pandas")
    install_module('pandas')
    import pandas as pd

# For time package 
try:
    import time
except ImportError:
    print("Trying to install required module: time")
    install_module("time")
    import time


# For numpy
    
try:
    import numpy as np
except ImportError:
    print("Trying to install required module: numpy")
    install_module("numpy")
    import numpy as np

# Global variable
count = 4

# Change the directory
os.chdir('/home/kamran/Link to CVM/AutoML/trigger/trigger_data')

# Read the Champaign file
camp_data = pd.read_csv('camp_data.csv')

# Show some data od the Champaign file
print("Some data of the Campaign")
print(camp_data.head())

#Checking the count of the each of the triggers and convert into the DataFrame
final_trigger_to_call = pd.DataFrame(camp_data.camp_Type.value_counts())
final_trigger_to_call = list(final_trigger_to_call[final_trigger_to_call.camp_Type >= count].index)
print("These are the following trigers")
print(final_trigger_to_call)

#Getting the trigger variable
trigger_variable_list = pd.read_csv('trigger_variables.csv')

# Save the triggers with its variables
m = {}
for i, j in zip(final_trigger_to_call,range(0,len(final_trigger_to_call))):
    m[i] = trigger_variable_list[final_trigger_to_call[j]]
    

# Showing the data for each Triggers    
for i in range(0, len(final_trigger_to_call)):
    columns = list(m.get(final_trigger_to_call[i]))
    #print(columns)
    columns=np.asarray(columns)
    df = pd.read_csv('trigger_data.csv',usecols=list(columns[columns!='nan']))
    print('Data for {0}'.format(final_trigger_to_call[i]))
    print(df.head())
    print("After droping the Empty Column")
    df.dropna(axis = 1, how = 'all', inplace = True)
    print(df.head())
    time.sleep(5)
    #df.head()
    


