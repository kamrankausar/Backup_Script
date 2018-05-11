#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 18:31:59 2018

@author: kamran
"""
#import the module
import pandas as pd
#import numpy as np
import datetime
#from datetime import date
import os
# read the dataset
os.chdir('/home/kamran/Link to CVM/AutoML/Test_Part')
df = pd.read_csv('credit_card.csv')

#Set the duration
day = 25
duration_days = datetime.timedelta(days = 25)

# Create the Suite which count the status of the Credit Card Payment
def credit_card_status_count(df_credit, duration_days):
    """ This suite take the DF and return DF with Payment status counts depending
    upon Payment date and Due date. 
    Levels of the credit_status_count = ['unpaid', 'delay', 'on_time'] on the 
    basis of duration (which is one of the arguments)
    Note duration must be in datetime.timedelta
    0.Convert the data type of the Date columns
    1.Create a column credit_paid_status which contains ['unpaid', 'delay', 'on_time'] 
    1.1 Create a function which takes two arguments CC_Due_Date and CC_Payment_Date and compare 
    this function does these
    CC_Payment_Date - CC_Due_Date if less than duration return on_time
    greater than duration return delay and unpaid if CC_Payment_Date is NaN
    2.Apply the logical operator to the date columns through lambda function  
    3. Apply groupby on cust_id and credit_status_count 
    4. Apply pivot function
    """
    #0
    df_credit['CC_Due_Date'] = df_credit['CC_Due_Date'].apply(lambda x: pd.to_datetime(x))
    df_credit['CC_Payment_Date'] = df_credit['CC_Payment_Date'].apply(lambda x: pd.to_datetime(x))
    #1
    df_credit['credit_paid_status'] = ''
    df_credit['temp_col'] = 0 # This col is created because it will use in the pivot table for value count
    #1.1
    def count_status(date1, date2):
        duration_days = datetime.timedelta(days = 25)
        if date1 - date2 > duration_days:
            return 'delay'
        elif date1 - date2 <= duration_days:
            return 'on_time'
        else:
            return 'unpaid'
    #2
    df_credit['credit_paid_status'] = df_credit.apply(lambda row: count_status(row['CC_Payment_Date'], row['CC_Due_Date']), axis = 1)
    #3
    df_credit = df_credit.groupby(['cust_id', 'credit_paid_status'], squeeze = True).count().reset_index()[['cust_id', 'credit_paid_status', 'temp_col']]
    df_credit = df_credit.pivot(index = 'cust_id', columns = 'credit_paid_status', values = 'temp_col').reset_index()
    #Return the dataFrame
    df_credit.fillna(0, inplace = True)
    return df_credit


#Call the function
    
df_return = credit_card_status_count(df, duration_days)
print('\n')
print('df_return')
print(df_return)
print('\ndf')
print(df)

