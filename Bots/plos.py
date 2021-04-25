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


def contrib(lista, categoria):
    # usage: contribuicao(lista, 7)
    
    categorias = [
        'Conceptualization',
        'Data curation',
        'Formal analysis',
        'Funding acquisition',
        'Investigation',
        'Methodology',
        'Project administration',
        'Resources',
        'Software',
        'Supervision',
        'Validation',
        'Writing – original draft',
        'Writing – review & editing'
    ]

    autores = []
    for author in lista:
        if re.findall(categorias[categoria], str(author[1])):
            autores.append(author[0])
                                 
    return ', '.join(autores)

df = pd.read_excel('plos_tratamento_inicial.xlsx', encoding='utf-8')


# Cols to Dataset
col_name = [
    'doi', 'eid', 'year', 'volume', 'issue', 'page_count', 'cited_by', 'title', 
    
    'authors_total',
    'authors_in_article', 
    'authors_id', 
    'authors', 
    
    'Conceptualization',
    'Data curation',
    'Formal analysis',
    'Funding acquisition',
    'Investigation',
    'Methodology',
    'Project administration',
    'Resources',
    'Software',
    'Supervision',
    'Validation',
    'Writing – original draft',
    'Writing – review & editing'   
]
   
article = {name:[] for name in col_name}

total_articles = df.shape[0]
count = 1
pause = 0
arq = 1

for index, row in df.iterrows():
    resp = requests.get('https://journals.plos.org/plosmedicine/article/authors?id=' + str(row.DOI))
    soup = BeautifulSoup(resp.text, 'html.parser')
    try:
        if len(soup.find_all("dd")) > 0:
            lista = []
            num_autores = len(soup.find_all("dd"))
            for x in soup.find_all("dl"):
                for c in range(0, num_autores):
                    autor = re.sub('(\n+)', '', x.find_all('dt')[c].text)
                    try:
                        contribuicao = re.sub('\s+', ' ', re.sub('\\n+|Roles|\s+', ' ', x.find_all('dd')[c].find_all('p', {'class':'roles'})[0].text)).strip()
                        lista.append([autor, contribuicao])
                    except:
                        pass
                    
            # Compila o byline (autores)
            byline_list = []
            for x,y in lista:
                byline_list.append(x)
            byline = '; '.join(byline_list)

            col = []

            col.append(row.DOI)
            col.append(row.EID)
            col.append(row.Year)
            col.append(row.Volume)
            col.append(row.Issue)
            col.append(row.Page_count)
            col.append(row.Cited_by)
            col.append(row.Title)

            col.append(row.authors_total)
            col.append(len(soup.find_all("dd"))) # authors_in_article
            col.append(row.Authors_ID)
            col.append(byline) # autores no byline

            col.append(contrib(lista, 0))
            col.append(contrib(lista, 1))
            col.append(contrib(lista, 2))
            col.append(contrib(lista, 3))
            col.append(contrib(lista, 4))
            col.append(contrib(lista, 5))
            col.append(contrib(lista, 6))
            col.append(contrib(lista, 7))
            col.append(contrib(lista, 8))
            col.append(contrib(lista, 9))
            col.append(contrib(lista, 10))
            col.append(contrib(lista, 11))
            col.append(contrib(lista, 12))

            for name, c in zip(col_name, col):
                article[name].append(c)
            print('Extracted:', str(count).zfill(4), '(', row.DOI, ') / ', total_articles)
            count += 1

            pause += 1
            if pause > 20:
            	df_article = pd.DataFrame(data=article)
            	df_article.to_csv('plos_scrap_' + str(arq).zfill(4) + '.csv', header=True, index=False, encoding='utf-8-sig')
            	arq += 1
            	
            	# pause to simulate a human
            	print("\n.... pausing 100 sec...\n")
            	time.sleep(100)
            	pause = 0

    except:
        print("Erro: ", row.DOI)



# Save data to file
df_article = pd.DataFrame(data=article)
df_article.to_csv('plos_scrap_final.csv', header=True, index=False, encoding='utf-8-sig')
