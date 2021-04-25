#!/usr/bin/env python
# coding: utf-8

# In[21]:


import re
import pandas as pd
import numpy as np

from matplotlib import pyplot
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import unicodedata

from scipy.interpolate import make_interp_spline, BSpline

import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)


# In[22]:


def by_line(N):
    byline = []
    for i in range(N):
        if(N == 1):
            byline.append( 0 )
        else:
            ret = byline.append( ( i/(N-1) ) )
    return byline

def contribuitor(df1, subscribers, item):
    for index, row in df1.iterrows():
        try:
            list = re.compile('|'.join(row[subscribers].split(', ')), re.UNICODE)
            
            if re.findall(list, row['author_name']):
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


# In[23]:


df = pd.read_excel('plos_tratado_333.xlsx', encoding='utf-8')
#df = df[(df['doi']=='10.1371/journal.pmed.1002785')]


# In[24]:


df.shape


# In[25]:


lista_autores = []
count = 0
columns = [
    'eid', 'doi', 'title', 'year', 'volume', 'issue', 'page_count', 'reader_count', 'export_saves_count', 'cited_by_count', 'clinical_cited_by_count',
    'all_blog_count', 'news_count', 'reference_count', 'comment_count', 'qa_site_mentions_count', 'facebook_count', 'tweet_count', 'abstract_views_count', 
    'full_text_views_count', 'link_click_count', 'link_outs_count', 'downloads_count',
    
    'author_in_article', 'authors', 'authors_id', 'author_id', 'author_name', 'author_byline', 'byline', 'posicao',

    'contrib_conceptualization',
    'contrib_data_curation',
    'contrib_formal_analysis',
    'contrib_funding_acquisition',
    'contrib_investigation',
    'contrib_methodology',
    'contrib_project_administration',
    'contrib_resources',
    'contrib_software',
    'contrib_supervision',
    'contrib_validation',
    'contrib_writing_original_draft',
    'contrib_writing_review_and_editing',
    
    'ac1', 'ac2', 'ac3', 'ac4', 'ac5', 'ac6', 'ac7', 'ac8', 'ac9', 'ac10', 'ac11', 'ac12', 'ac13',
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

                row['contrib_conceptualization'], # contrib_authors_study_concept_and_design
                row['contrib_data_curation'], # contrib_authors_critical_revision
                row['contrib_formal_analysis'], # contrib_authors_drafting_manuscript
                row['contrib_funding_acquisition'], # contrib_authors_study_supervision            
                row['contrib_investigation'], # contrib_authors_administrative_support           
                row['contrib_methodology'], # contrib_authors_obtained_funding            
                row['contrib_project_administration'], # contrib_authors_acquisition_analysis_interpretation_data            
                row['contrib_resources'], # contrib_authors_analysis_interpretation_data
                row['contrib_software'], # contrib_authors_analysis_interpretation_data
                row['contrib_supervision'], # contrib_authors_acquisition_data
                row['contrib_validation'],
                row['contrib_writing_original_draft'],
                row['contrib_writing_review_and_editing'],

                contribuicao(''.join(autores[count].split(',')), row['contrib_conceptualization'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_data_curation'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_formal_analysis'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_funding_acquisition'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_investigation'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_methodology'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_project_administration'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_resources'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_software'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_supervision'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_validation'], row['contrib_validation']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_writing_original_draft'], row['authors_in_article']),
                contribuicao(''.join(autores[count].split(',')), row['contrib_writing_review_and_editing'], row['authors_in_article']),
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
ac11 = 0
ac12 = 0
ac13 = 0
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
        ac11 += r['ac11']
        ac12 += r['ac12']
        ac13 += r['ac13']

print(round(ac1,6), round(ac2,6), round(ac3,6), round(ac4,6), round(ac5,6), round(ac6,6), round(ac7,6), round(ac8,6), round(ac9,6), round(ac10,6), round(ac11,6), round(ac12,6), round(ac13,6))
# In[26]:


df1.to_excel("plos_compilado.xlsx", header=True, index=False, encoding='utf-8')
print('Done!')


# In[28]:


df_byline = pd.read_excel('plos_compilado.xlsx', encoding='utf-8')
df_autores = pd.read_excel('plos_authors_3740.xlsx', encoding='utf-8')
resultado = pd.merge(df_byline, df_autores, on='author_id', how='inner')
resultado.to_excel("plos_final.xlsx", header=True, index=False, encoding='utf-8')


# In[ ]:




