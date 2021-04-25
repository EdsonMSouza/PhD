#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import pandas as pd
import numpy as np
import operator

from matplotlib import pyplot
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import unicodedata

from scipy.interpolate import make_interp_spline, BSpline

import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)


# In[ ]:


def by_line(N):
    byline = []
    for i in range(N):
        if(N == 1):
            byline.append( 0 )
        else:
            ret = byline.append( ( i/(N-1) ) )
    return byline

def contribuitor_(df1, subscribers, item):
    for index, row in df1.iterrows():
        try:
            list = re.compile('|'.join(row[subscribers].split(',')), re.UNICODE)
            
            if row[subscribers] == 'All authors':
                df1.at[index, 'ac' + str(item)] =  1
            
            elif re.findall(list, row['author_name']):
                df1.at[index, 'ac' + str(item)] =  1
        except:
            pass
    return df1

# inclui o strip(" ") para remover os espaços em branco antes dos nomes
def contribuicao(author_name, autores, qtd):
    retorno = 0
    try:
        list = re.compile('|'.join(autores.split(',')), re.UNICODE)
        
        if autores == 'All authors':
            retorno = 1/qtd
        else:
            try:
                for a in autores.split(","):
                    try:
                        if re.findall(list, autores):
                            if(re.findall(a.strip(" "), author_name)): # (a, author_name)
                                if(len(autores.split(",")) > 0):
                                    retorno = 1/len(autores.split(","))
                    except:
                        retorno = 0
            except:
                retorno = 0
    except:
        retorno = 0
        
    return retorno

# calcula a repetição de palavras em uma sequência de caracteres
def popularidade(texto, palavra):
    import re
    return sum(1 for _ in re.finditer(r'\b%s\S' % re.escape(palavra), texto)) #\b é o original

def contaSobrenomes(autores):
    r = max(dict([v, popularidade(autores, v)] 
         for v in autores.split("; ")).items(), key=operator.itemgetter(1))
    
    if r[1] > 1:
        return r


# In[ ]:


df = pd.read_excel('jama_tratado.xlsx', encoding='utf-8')
#df = df[(df['doi']=='10.1001/jama.2013.5827')]


# In[ ]:


df.shape


# In[ ]:


lista_autores = []
count = 0
columns = [
    'eid', 'doi', 'title', 'year', 'volume', 'issue', 'page_count', 'reader_count', 'export_saves_count', 'cited_by_count', 'clinical_cited_by_count',
    'all_blog_count', 'news_count', 'reference_count', 'comment_count', 'qa_site_mentions_count', 'facebook_count', 'tweet_count', 'abstract_views_count', 
    'full_text_views_count', 'link_click_count', 'link_outs_count', 'downloads_count', 'authors_in_article', 
    
    'authors', 'authors_id', 'author_id', 'author_name', 'author_byline', 'byline', 'posicao',
    
    'corresponding_author', 
    'author_responsability',

    'contrib_authors_study_concept_and_design', 
    'contrib_authors_critical_revision', 
    'contrib_authors_drafting_manuscript', 
    'contrib_authors_statistical_analysis', 
    'contrib_authors_study_supervision', 
    'contrib_authors_administrative_support', 
    'contrib_authors_obtained_funding', 
    'contrib_authors_acquisition_analysis_interpretation_data', 
    'contrib_authors_analysis_interpretation_data', 
    'contrib_authors_acquisition_data',
    
    'ac1', 'ac2', 'ac3', 'ac4', 'ac5', 'ac6', 'ac7', 'ac8', 'ac9', 'ac10', 'flag'
]

for index, row in df.iterrows():
    ids = row['authors_id'].split('; ')
    autores = row['authors'].split('; ')
    
    try:
        for linha in range(len(ids)):
            lista_autores.append([
                row['eid'],
                row['doi'],
                row['title'],
                row['year'],
                row['volume'],
                row['issue'],
                row['page_count'],
                row['reader_count'],
                row['export_saves_count'],
                row['cited_by_count'],
                row['clinical_cited_by_count'],
                row['all_blog_count'],
                row['news_count'],
                row['reference_count'],
                row['comment_count'],
                row['qa_site_mentions_count'],
                row['facebook_count'],
                row['tweet_count'],
                row['abstract_views_count'],
                row['full_text_views_count'],
                row['link_click_count'],
                row['link_outs_count'],
                row['downloads_count'],
                row['authors_in_article'],
                row['authors'],
                row['authors_id'],
                str(''.join(ids[count].split(' '))), # author_id            
                ' '.join(autores[count].split(' ')), # author_name
                str((by_line(len(ids))[count])).replace(',', '.'), # author_byline

                str((by_line(len(ids)))).replace('.', '.').strip('[]'), #byline

                count+1, # author_position

                row['corresponding_author'], 
                row['author_responsability'],

                row['contrib_authors_study_concept_and_design'], # contrib_authors_study_concept_and_design
                row['contrib_authors_critical_revision'], # contrib_authors_critical_revision
                row['contrib_authors_drafting_manuscript'], # contrib_authors_drafting_manuscript
                row['contrib_authors_statistical_analysis'], # contrib_authors_statistical_analysis
                row['contrib_authors_study_supervision'], # contrib_authors_study_supervision
                row['contrib_authors_administrative_support'], # contrib_authors_administrative_support
                row['contrib_authors_obtained_funding'], # contrib_authors_obtained_funding
                row['contrib_authors_acquisition_analysis_interpretation_data'], # contrib_authors_acquisition_analysis_interpretation_data
                row['contrib_authors_analysis_interpretation_data'], # contrib_authors_analysis_interpretation_data
                row['contrib_authors_acquisition_data'], # contrib_authors_acquisition_data   

                contribuicao(''.join(autores[count].split(',')), row['contrib_authors_study_concept_and_design'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_authors_critical_revision'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_authors_drafting_manuscript'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_authors_statistical_analysis'],row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_authors_study_supervision'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_authors_administrative_support'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_authors_obtained_funding'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_authors_acquisition_analysis_interpretation_data'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_authors_analysis_interpretation_data'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_authors_acquisition_data'], row['authors_in_article']),


                #0, # contrib_study_concept_and_design
                #0, # contrib_critical_revision
                #0, # contrib_drafting_manuscript
                #0, # contrib_statistical_analysis
                #0, # contrib_study_supervision
                #0, # contrib_administrative_support
                #0, # contrib_obtained_funding'
                #0, # contrib_acquisition_analysis_interpretation_data'
                #0, # contrib_analysis_interpretation_data'
                #0 # contrib_acquisition_data

                contaSobrenomes(row['authors']) # flag para verificação de sobrenomes duplicados

            ])
            count += 1
        count = 0
    except:
        print('Erro', ' '.join(autores[count].split(',')), row['authors'])

df1 = pd.DataFrame(data=lista_autores, columns=columns)
print('Done!')

ac1  = 0
ac2  = 0
ac3  = 0
ac4  = 0
ac5  = 0
ac6  = 0
ac7  = 0
ac8  = 0
ac9  = 0
ac10 = 0
for i, r in df1.iterrows():
        ac1  += r['ac1']
        ac2  += r['ac2']
        ac3  += r['ac3']
        ac4  += r['ac4']
        ac5  += r['ac5']
        ac6  += r['ac6']
        ac7  += r['ac7']
        ac8  += r['ac8']
        ac9  += r['ac9']
        ac10 += r['ac10']

print(round(ac1,6), round(ac2,6), round(ac3,6), round(ac4,6), round(ac5,6), round(ac6,6), round(ac7,6), round(ac8,6), round(ac9,6), round(ac10,6))
# In[ ]:


df1.to_excel("jama_compilado.xlsx", header=True, index=False, encoding='utf-8')
print('Done!')


# In[ ]:


df_byline = pd.read_excel('jama_compilado.xlsx', encoding='utf-8')
df_autores = pd.read_excel('jama_authors_13087.xlsx', encoding='utf-8')

resultado = pd.merge(df_byline, df_autores, on='author_id', how='inner')

resultado.to_excel("jama_final_7780.xlsx", header=True, index=False, encoding='utf-8')


# In[ ]:




