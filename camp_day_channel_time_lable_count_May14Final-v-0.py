#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 15:48:04 2018

@author: kamran
"""
#import the moduel
import pandas as pd
import numpy as np
import os
from functools import reduce # For merging more than one DataFrame in Py3

#Change the directory
os.chdir('/home/kamran/Link to CVM/AutoML/Test_Part')
# Getting the data 
df = pd.read_csv('camp_response_data.csv')

# Creating the Suit name camp_cha_day_time_count(df)

def camp_cha_day_time_count(df):
    """
    This suite takes the DF as input and does following things
    1. Aggregate the days at Customer Level and save in DF
    2. Aggregate the channel at Custome Level and save in DF
    3. Aggregate the time_lable at Custome Level and Save in DF
    4. Merge all the above DF on the basis of Customer
    """
    #Change the data type of the response time to datetime stamp
    df['camp_response_time'] = pd.to_datetime(df['camp_response_time'], errors='coerce')
    # Create the needed columns
    #Create the day and time(hour, min) column
    df.res_day = np.nan
    #df.resp_time = np.nan
    df.res_hr = np.nan
    df.res_min = np.nan
    df['day_counts'] = 0
    df['cha_count'] = 0
    # 1.Aggregate the days at Customer Level and save in df_day_count
    #Extract day from the camp_response_time
    df['res_day'] = df.camp_response_time.dt.weekday_name
    df_day_count = df.groupby(['cust_id', 'res_day'], squeeze = True).count().reset_index()[['cust_id', 'res_day', 'day_counts']]
    df_day_count = df_day_count.pivot(index = 'cust_id', columns = 'res_day', values = 'day_counts').reset_index()
    df_day_count.fillna(0, inplace = True)
    # 2.Aggregate the channel at Custome Level and save in df_cha_count
    df_cha_count = df.groupby(['cust_id', 'camp_channel_type'], squeeze = True).count().reset_index()[['cust_id', 'camp_channel_type', 'cha_count']]    
    df_cha_count = df_cha_count.pivot(index = 'cust_id', columns = 'camp_channel_type', values = 'cha_count').reset_index()
    df_cha_count.fillna(0, inplace = True)
    
    #3.3. Aggregate the time_lable at Custome Level and Save in df_time_lable_count
    df.res_time_lable = np.nan
    df['lable_count'] = 0
    df['res_hr'] = df.camp_response_time.dt.hour
    df['res_min'] = df.camp_response_time.dt.minute
    #Response Lable
    def res_lable(get_hour, get_min):
        ''' 
        1. 0 <-> 6:30 = Early Morning
        2. 6:31 <-> 9:30 = Work_Coming_Time
        3. 9:31 <-> 12:30 = Work_peak_Time
        4. 12:31 <-> 15:30 = Lunch_Time 
        5. 15:31 <-> 18:30 = Post_lunch_Time
        6. 18:31 <-> 20:30 = Going_Home_Time
        7. 20:30 <-> 23:59 = DND_Family_Time
        '''
        mins = int(get_hour) * 60 + int(get_min)
        if 0 <= mins <= 390:
            return 'early_morning'
        elif 391 <= mins <= 570:
            return 'office_comming_time'
        elif 571 <= mins <= 750:
            return 'office_peak_time'
        elif 751 <= mins <= 930:
            return 'lunch_time'
        elif 931 <= mins <= 1110:
            return 'post_lunch'
        elif 1111 <= mins <= 1230:
            return 'going_home_time'
        elif 1231 <= mins <= 1439:
            return 'office_peak_time'
        else:
            return 'nan'
    df['res_time_lable'] = df.apply(lambda row : res_lable(row.res_hr, row.res_min), axis = 1)
    # Doing the groupby
    df_time_lable_count = df.groupby(['cust_id', 'res_time_lable'], squeeze = True).count().reset_index()[['cust_id', 'res_time_lable', 'lable_count']]
    df_time_lable_count = df_time_lable_count.pivot(index = 'cust_id', columns = 'res_time_lable', values = 'lable_count').reset_index()
    df_time_lable_count.fillna(0, inplace = True)
    #Merge all the new DataFrame
    #1.df_day_count 
    #2.df_cha_count
    #3.df_time_lable_count 
    dfs = [df_day_count, df_cha_count, df_time_lable_count]
    df_final = reduce(lambda left,right: pd.merge(left,right,on='cust_id'), dfs)
    return df_final


df_get = camp_cha_day_time_count(df)
print(df_get)
    
    

    
    
    
    
    
    
    