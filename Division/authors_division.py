#!/usr/bin/env python
# coding: utf-8

# <h1>Extract Author's ID from Article's Source</h1>
# <h3>Author: Edson Melo de Souza (souzaem@uni9.pro.br)</h3>
# Review 0: February, 26th 2019

# <h1>Description</h1>
# This module extracts Author(s) ID from Article Source File
# <ul>
#     <li>An archive of each area containing the author IDs is recorded</li>
#     <li>The file "#totals.txt" contains the totals by area</li>
# </ul>

# <hr>

# ### Import Modules

# In[1]:


import pandas as pd
import numpy as np
import sqlite3
import os
import shutil


# ### Function Definition

# In[23]:


def extract_author_id(file):
    scopus_df = pd.read_excel(file + '.xlsx')
    
    # split author's ID from Author(s) ID colum 
    authorsID = scopus_df['Author(s) ID'].str.split(';').tolist()
    
    # build a list with separated authors
    list_authorsID = []

    for listIDs in authorsID:
        for item in listIDs:
            list_authorsID.append(''.join(item.split(' ')))
            
    header = ['author_id']
    general_count = len(list_authorsID)
    unique_count = len(set(list_authorsID))
    
    # save list with no repeated authors
    import csv
    with open('extracted_authors_' + file + '.csv', 'w') as csvFile:
        wr = csv.writer(csvFile, delimiter='\n')
        wr.writerow(set(header))
        wr.writerow(set(list_authorsID))
    
    csvFile.close()
    
    return general_count, unique_count, set(list_authorsID)


# In[24]:


# Delete old files
path = "./"
dir = os.listdir(path)
for file in dir:
    if file == "authors.db":
        os.remove(file)
    if file == "": 
        os.remove(file)

file = 'data_articles'
general_count, unique_count, _ = extract_author_id(file)
#unique_count


# In[25]:


# Load save data
df = pd.read_csv('extracted_authors_data_articles.csv')


# In[26]:


# Export to sqlite format
df['processed'] = 0
cnx = sqlite3.connect('authors.db')
df.to_sql(name='authors', con=cnx, index=False)


# In[2]:


df = pd.read_excel('data_articles.xlsx')
df = df[['DOI', 'EID']]


# In[4]:


# Export doi, eid
path = "./"
dir = os.listdir(path)
for file in dir:
    if file == "plumx.db":
        os.remove(file)
    if file == "": 
        os.remove(file)
        
df['processed'] = 0
cnx = sqlite3.connect('plumx.db')
df.to_sql(name='journals', con=cnx, index=False)


# In[ ]:




