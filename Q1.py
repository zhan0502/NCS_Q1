#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import glob
from datetime import datetime

appended_data = []

#Step 1: process csv files in raw data folder one by one
for file in glob.glob('raw/*.csv'):
    print('Processing ' + file + " ...") 
    df = pd.read_csv(file)
    
    #Step 2: delete the rows which do not contain a name
    df = df.dropna(axis=0, subset=['name'])
    
    #Step 3. split the name column  into first and last columns.
    df['name'] = df['name'].replace(['Miss ','Mr\. ','Ms\. ', 'Dr\.'],'', regex=True) #remove prefix using regular expression
    df[['first_name','last_name']] = df['name'].loc[df['name'].str.split().str.len() == 2].str.split(expand=True)
    df['first_name'].fillna(df['name'],inplace=True)
    df=df.drop(['name'], axis=1)
    df=df[['first_name', 'last_name', 'price']]
    
    #Step 4. ensure the price column contains only numbers
    if not pd.to_numeric(df['price'], errors='coerce').notnull().all():
        df = df[pd.to_numeric(df['price'], errors='coerce').notnull()]
    df['price'] = pd.to_numeric(df['price'])
    
    #Step 5: add a new column, which will be true if the price is greater than 100, and false otherwise.
    df['price greater than 100'] = df['price'].ge(100)
    appended_data.append(df)

#Step 6: output the processed dataframe to a timestamped csv file
appended_data = pd.concat(appended_data, ignore_index=True, sort=False)
time = datetime.now().strftime("%Y%m%d-%H%M%S")
appended_data.to_csv('output_'+ time +'.csv', index=False)
print('Processing is completed! Please check output file.')

