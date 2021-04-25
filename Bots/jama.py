from bs4 import BeautifulSoup
from pathlib import Path
from random import *
from xml.etree import ElementTree as ET

import unicodedata
import contextlib 
import json
import numpy as np
import os
import pandas as pd
import re
import requests
import sqlite3
import sys
import time
import timeit


# # JAMA Contributions Categories

# In[ ]:


categories = [
    ['Study concept and design: ', '([.*])|(\s+)|(Study concept and design: )'],    
    ['Critical revision of the manuscript for important intellectual content: ', '([.*])|(\s+)|(Critical revision of the manuscript for important intellectual content: )'],
    ['Drafting of the manuscript: ', '([.*])|(\s+)|(Drafting of the manuscript: )'],
    ['Statistical analysis: ', '([.*])|(\s+)|(Statistical analysis: )'],
    ['Study supervision: ', '([.*])|(\s+)|(Study supervision: )'],
    ['Administrative, technical, or material support: ', '([.*])|(\s+)|(Administrative, technical, or material support: )'],
    ['Obtained funding: ', '([.*])|(\s+)|(Obtained funding: )'],
    ['Acquisition, analysis, or interpretation of data: ', '([.*])|(\s+)|(Acquisition, analysis, or interpretation of data: )'],    
    ['Analysis and interpretation of data: ', '([.*])|(\s+)|(Analysis and interpretation of data: )'],    
    ['Acquisition of data: ', '([.*])|(\s+)|(Acquisition of data: )']
]


# # Functions

# In[ ]:


def authors(soup):
    _authors = []
    authors_list = soup.find(class_='meta-authors')
    authors = authors_list.find_all('a')

    for author in authors:
        if (author.text != 'et al'):
            _authors.append(unicodedata.normalize("NFKD", re.split(',', author.text)[0]))
    return '; '.join(_authors)

def corresponding_author(soup):
    try:
        corresponding_author = soup.find(class_='authorInfoSection')
        author = corresponding_author.text[22:]
        return re.sub('(\n+\s+)', ' ', re.split(',', author, 1)[0])
    except:
        pass
    
def corpus(soup):
    try:
        corpus = ''
        article = soup.find(class_='widget-ArticleFulltext widget-instance-AMA_Article_FullText_Widget')
        for content in article.find_all('p',{'class':'para'}):   
            if re.search('Author Contributions: ', content.text):
                break
            corpus = corpus + content.text
            
        return re.sub('(\n+\s+)', ' ', corpus)
    except:
        pass
    
def contribuitions(soup, item):
    try:
        lista = []
        authors_list = soup.find(class_='widget-ArticleFulltext widget-instance-AMA_Article_FullText_Widget')
      
        for line in authors_list.find_all('p',{'class':'para'}):
            if re.findall(categories[item][0], line.text):       
                lista.append(re.sub(categories[item][1], '', line.text))
                
        return ''.join(lista)

    except:
        pass
    
def responsability(soup):
    try:
        authors_list = soup.find(class_='widget-ArticleFulltext widget-instance-AMA_Article_FullText_Widget')
        for line in authors_list.find_all('p',{'class':'paraauthor-contributions'}):
            if re.findall('(Author Contributions)|(AuthorContributions: )', line.text):
                return re.sub('([.*])|(\s+)|(Author Contributions: )|(AuthorContributions: )', ' ', line.text)
            
        for line in authors_list.find_all('p',{'class':'para'}):
            if re.findall('(Author Contributions)|(AuthorContributions: )', line.text):      
                return re.sub('([.*])|(\s+)|(Author Contributions: )|(AuthorContributions: )', ' ', line.text)
    except:
        pass


# # Selenium config

# In[ ]:


# Selenium config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("Retry-After: 3600")
options.add_argument("Accept':'text/html")
chrome = webdriver.Chrome(options=options)


# In[ ]:


# Load dataset
df = pd.read_excel('medicine_tratado.xlsx', encoding='utf-8')


# # Extraction

# In[ ]:


# Cols to Dataset
col_name = [
    'doi', 'eid', 'year', 'volume', 'issue', 'page_count', 'cited_by', 'title',
    'authors_number', 'authors_id', 'authors', 
    'corresponding_author', 'author_responsability',
    
    'contrib_study_concept_and_design', 
    'contrib_critical_revision', 
    'contrib_drafting_manuscript', 
    'contrib_statistical_analysis', 
    'contrib_study_supervision', 
    'contrib_administrative_support', 
    'contrib_obtained_funding', 
    'contrib_acquisition_analysis_interpretation_data', 
    'contrib_analysis_interpretation_data', 
    'contrib_acquisition_data',
    'corpus']
   
article = {name:[] for name in col_name}

total_articles = df.shape[0]
count = 1
pause = 0
arq = 3

for index, row in df.iterrows():
    chrome.get('https://dx.doi.org/' + str(row.DOI))
    soup = BeautifulSoup(chrome.page_source, 'html.parser')    
    try:
        if len(soup.find_all('p',{'class':'para'})) > 0: 
            col = []

            col.append(row.DOI)
            col.append(row.EID)
            col.append(row.Year)
            col.append(row.Volume)
            col.append(row.Issue)
            col.append(row.Page_count)
            col.append(row.Cited_by)
            col.append(row.Title)            

            col.append(len(authors(soup).split('; ')))
            col.append(row.Authors_ID)
            col.append(authors(soup))

            col.append(corresponding_author(soup))
            col.append(responsability(soup))

            col.append(contribuitions(soup, 0))
            col.append(contribuitions(soup, 1))
            col.append(contribuitions(soup, 2))
            col.append(contribuitions(soup, 3))
            col.append(contribuitions(soup, 4))
            col.append(contribuitions(soup, 5))
            col.append(contribuitions(soup, 6))
            col.append(contribuitions(soup, 7))
            col.append(contribuitions(soup, 8))
            col.append(contribuitions(soup, 9))
            col.append(corpus(soup))

            for name, c in zip(col_name, col):
                article[name].append(c)
            print('Extracted:', str(count).zfill(4), '/', total_articles)
            count += 1

            time.sleep(10)

            pause += 1
            if pause > 20:
                # Save partial data to file
                df_article = pd.DataFrame(data=article)
                df_article.to_csv('jama_data_' + str(arq).zfill(4) + '.csv', header=True, index=False, encoding='utf-8-sig')
                arq += 1
                # pause to simulate a human
                print("\n.... pausing 300 sec...\n")
                time.sleep(300)
                pause = 0
    except:
        pass

# Save data to file
df_article = pd.DataFrame(data=article)
df_article.to_csv('jama_data_final.csv', header=True, index=False, encoding='utf-8-sig')

