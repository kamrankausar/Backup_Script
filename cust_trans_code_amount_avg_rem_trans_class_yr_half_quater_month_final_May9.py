#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 13:48:50 2018

@author: kamran
"""

# importing Library
import pandas as pd
import numpy as np
import os
import datetime
from datetime import date
# Change the directory
os.chdir('/home/kamran/Link to CVM/AutoML/Test_Part')
# Reading the file
df = pd.read_csv('trans_type_amount_date_time_test.csv')
df['trans_time'] = df.trans_time.apply(lambda x : pd.to_datetime(x))
df.head()
df.dtypes
need_trans_classes = ['debit','credit','debit_card_withdrawal','credit_card_withdrawal']
df.trans_code.value_counts()
# Getting the todays date


#Duration limit of the Transaction i.e before 1 year
#Duration will be pass as the duration to the the count_trans_type_avg_amount suit 
duration_yearly = datetime.timedelta(days=365)

#Creating the suit for Transaction type and its average amount by 
#customer Id
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#Function Return duration yearly
def count_trans_type_avg_amount_duration(df, duration_time, need_trans_classes):
    """This suit get the data farme as its arguement and 
    return the df after doing these type of calculation
    
    0. Filter the rows of the transaction between the duration yearly period.
    0.1 Get only that rows which contains classes what we need 
    1. Count the Transaction type according to the customer 
    2. Then claculate the average transasction amount 
    3. """
    #Get today date
    now = pd.to_datetime(str(date.today()), format='%Y-%m-%d')
    #Filter the rows of the transaction between the duration period.
    duration = datetime.timedelta(days=duration_time)
    df = df[now - df['trans_time'] <= duration]
    # Get only that rows which contains classes what we need
    #Get all the classes from Transaction Features and save as list
    trans_all_classes = list(df.trans_code.value_counts().index)
    remove_trans_classes = list(set(trans_all_classes) - set(need_trans_classes))
    for i in range(0, len(remove_trans_classes)):
        df = df.drop(df[(df.trans_code == remove_trans_classes[i])].index)
    # Find the count of Credit and withdrawl for each customer - Table name =type_count_raw
    type_count_raw = df.groupby(['cust_id', 'trans_code'], squeeze = True).count().reset_index()[['cust_id','trans_code','trans_time']]
    #Okay
    type_count = type_count_raw.pivot(index='cust_id', columns='trans_code', values='trans_time').reset_index()
    oper_avg = (pd.pivot_table(df, index = 'cust_id', columns= 'trans_code', values = 'trans_amount',aggfunc = np.average)).reset_index()
    type_oper_avg = pd.merge(type_count, oper_avg,suffixes=('_count', '_avg'), how='right', on='cust_id')
    return type_oper_avg

# Calling the Suite    
df_test_yearly = count_trans_type_avg_amount_duration(df, 365, need_trans_classes)
df_test_half = count_trans_type_avg_amount_duration(df, 180, need_trans_classes)
df_test_quaterly = count_trans_type_avg_amount_duration(df, 90, need_trans_classes)
df_test_monthly = count_trans_type_avg_amount_duration(df, 30, need_trans_classes)
df_test_yearly.head()
df_test_half.head()
df_test_quaterly.head()
df_test_monthly.head()


