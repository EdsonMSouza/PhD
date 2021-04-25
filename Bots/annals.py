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


def byline(soup):
    return re.sub('\n+', '', soup.find('p', {'class':'authors js-article-authors'}).text).strip()


categories = [
        ['Conception and design','Author Contributions: Conception and design:|Author Contributions: Conception and design.'],
        ['Analysis and interpretation of the data','Analysis and interpretation of the data: |Analysis and interpretation of the data. '],
        ['Drafting of the article','Drafting of the article: |Drafting of the article. '],
        ['Critical revision for important intellectual content','Critical revision for important intellectual content: |Critical revision for important intellectual content. '],
        ['Final approval of the article','Final approval of the article: |Final approval of the article. '],
        ['Statistical expertise','Statistical expertise: |Statistical expertise. '],
        ['Obtaining of funding','Obtaining of funding: |Obtaining of funding. '],
        ['Administrative, technical, or logistic support','Administrative, technical, or logistic support: |Administrative, technical, or logistic support. '],
        ['Collection and assembly of data','Collection and assembly of data: |Collection and assembly of data. '],
        ['Provision of study materials or patients','Provision of study materials or patients: |Provision of study materials or patients. ']
    ]

def contribuitions(soup, item):
    dados = []
    lista = []
    for categorias in soup.find_all('ul', {'class':'wi-affiliationList ati-toggle-content hide'}):
        for line in categorias.find_all('p'):
            dados.append(line.text)
            
        for line in dados:
            if re.findall(categories[item][0], line):
                lista.append(re.sub(categories[item][1], '', line).strip()[:-1])
                
        return ''.join(lista)


# # Extraction

# In[ ]:


# Load dataset
df = pd.read_excel('annals_tratado.xlsx', encoding='utf-8')


# In[ ]:


col_name = [    
    'doi', 'eid', 'year', 'volume', 'issue', 'page_count', 'cited_by', 'title',     
    
    'authors_total',
    'authors_in_article', 
    'authors_id', 
    'authors',     
    
    'contrib_conception_and_design', 
    'contrib_analysis_and_interpretation_of_the_data', 
    'contrib_drafting_of_the_article', 
    'contrib_critical_revision_for_important_intellectual_content', 
    'contrib_final_approval_of_the_article', 
    'contrib_statistical_expertise', 
    'contrib_obtaining_of_funding', 
    'contrib_administrative_technical_or_logistic_support', 
    'contrib_collection_and_assembly_of_data', 
    'contrib_provision_of_study_materials_or_patients'
]
   
article = {name:[] for name in col_name}

total_articles = df.shape[0]
count = 1
pause = 0
arq = 1

for index, row in df.iterrows():
    chrome.get('https://dx.doi.org/' + str(row.doi))
    soup = BeautifulSoup(chrome.page_source, 'html.parser')    
    try:
        #if len(soup.find_all('p',{'class':'wi-affiliationList ati-toggle-content hide'})) > 0: 
        col = []

        col.append(row.doi)
        col.append(row.eid)
        col.append(row.year)
        col.append(row.volume)
        col.append(row.issue)
        col.append(row.page_count)
        col.append(row.cited_by)
        col.append(row.title)

        col.append(row.authors_total)
        col.append(len(byline(soup).split('; '))) # total de autores no artigo
        col.append(row.authors_id)
        col.append(byline(soup))

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

        for name, c in zip(col_name, col):
            article[name].append(c)
        print('Extracted:', str(count).zfill(4), '/', total_articles)
        count += 1

        pause += 1
        if pause > 100:
            df_article = pd.DataFrame(data=article)
            df_article.to_csv('annals_scrap_' + str(arq).zfill(4) + '.csv', header=True, index=False, encoding='utf-8-sig')
            arq += 1

            # pause to simulate a human
            print("\n.... pausing 10 sec...\n")
            time.sleep(10)
            pause = 0
    except:
        print("Err: ", row.doi)


# In[ ]:


# Save data to file
df_article = pd.DataFrame(data=article)
df_article.to_csv('annals_scrap.csv', header=True, index=False, encoding='utf-8-sig')
