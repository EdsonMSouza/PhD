#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd


# In[15]:


# Function to sanitize fields
def fix_int(x):
    try:
        return int(x)
    except ValueError:
        return 0
    
def big_values(x):
    r = 0
    if(x < 999):
        r = x
    else:
        r = 0
    return r

def page_count(x):    
    r = 0
    if( x < 0):
        r = 0
    else:
        r = x
    return r


# In[16]:


# Load data
df = pd.read_csv('scopus.csv')


# In[17]:


# Delete articles with name nonexistent authors
df.drop(df[df['Authors']=='[No author name available]'].index, inplace=True)


# In[18]:


# Delete articles without authors' ID
df.drop(df[df['Author(s) ID']=='[No author name available]'].index, inplace=True)


# In[19]:


# Count total Authors in article
obj = []
for i, t in df.iterrows():
    obj.append(len(t['Author(s) ID'].split('; ')))


# In[20]:


df['Total'] = obj
df.fillna(0, inplace=True)


# In[21]:


# Delete all lines less four authors
df.drop(df[df['Total'] < 4].index, inplace=True)


# In[22]:


# Delete lines without DOI
df.drop(df[df['DOI'].isnull()].index, inplace=True)
df.drop(df[df['DOI'] == 0].index, inplace=True)


# In[23]:


# Delete Page count field 
del df['Page count']


# In[24]:


# Sanitize fields
df['page_start'] = df['Page start'].replace(r'[^0-9]', '', regex=True, inplace = False)
df['page_start'] = df['page_start'].apply(fix_int).dropna()
df['page_start'].astype(int)

df['page_end'] = df['Page end'].replace(r'[^0-9]', '', regex=True, inplace = False)
df['page_end'] = df['page_end'].apply(fix_int).dropna()
df['page_end'].astype(int)

df['page_count'] = df['page_end'] - df['page_start']
df['page_count'] = df['page_count'].apply(page_count)
df['page_count'] = df['page_count'].apply(big_values)


# In[25]:


# Delete old fields
del df['Page start']
del df['Page end']


# In[26]:


# Save processed dataset
df.to_excel('data_articles.xlsx', index=False)

