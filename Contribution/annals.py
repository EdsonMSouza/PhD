#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import operator
import numpy as np
import pandas as pd
import unicodedata

import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

from IPython.core.debugger import set_trace


# In[2]:


def by_line(N):
    byline = []
    for i in range(N):
        if(N == 1):
            byline.append( 0 )
        else:
            ret = byline.append( ( i/(N-1) ) )
    return byline

# calcula a repetição de palavras em uma sequência de caracteres
def popularidade(texto, palavra):
    import re
    return sum(1 for _ in re.finditer(r'\b%s\S' % re.escape(palavra), texto)) #\b é o original

def contaSobrenomes(autores):
    r = max(dict([v, popularidade(autores, v)] 
         for v in autores.split("; ")).items(), key=operator.itemgetter(1))
    
    if r[1] > 1:
        return r

# inclui o strip(" ") para remover os espaços em branco antes dos nomes
def contribuicao(author_name, autores_novos, autores):
    retorno = 0
    list = re.compile('|'.join(autores_novos.split('; ')), re.UNICODE)
    try:
        for a in autores.split("; "):
            try:
                if re.findall(list, autores):
                    if(re.findall(a.strip(" "), author_name)): # (a, author_name)
                        if(len(autores.split("; ")) > 0):
                            retorno = 1/len(autores.split("; "))
            except:
                retorno = 0
    except:
        retorno = 0
        
    return retorno


# In[3]:


df = pd.read_excel('annals_tratado.xlsx', encoding='utf-8')


# In[259]:


#df = df[(df['doi']=='10.7326/M18-1529')]


# In[4]:


df.shape


# In[261]:


lista_autores = []
count = 0
columns = [
    'eid', 'doi', 'title', 'year', 'volume', 'issue', 'page_count', 'reader_count', 'export_saves_count', 'cited_by_count', 'clinical_cited_by_count',
    'all_blog_count', 'news_count', 'reference_count', 'comment_count', 'qa_site_mentions_count', 'facebook_count', 'tweet_count', 'abstract_views_count', 
    'full_text_views_count', 'link_click_count', 'link_outs_count', 'downloads_count',
    
    'author_in_article', 'authors', 'autores_novos', 'authors_id', 'author_id', 'author_name', 'author_byline', 'byline', 'posicao',

    'contrib_conception_and_design', 
    'contrib_analysis_and_interpretation_of_the_data', 
    'contrib_drafting_of_the_article', 
    'contrib_critical_revision_for_important_intellectual_content', 
    'contrib_final_approval_of_the_article', 
    'contrib_statistical_expertise', 
    'contrib_obtaining_of_funding', 
    'contrib_administrative_technical_or_logistic_support', 
    'contrib_collection_and_assembly_of_data', 
    'contrib_provision_of_study_materials_or_patients',
    'c1',
    'c2',
    'c3',
    'c4',
    'c5',
    'c6',
    'c7',
    'c8',
    'c9',
    'c10',
    
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
                row['autores_novos'],
                row['authors_id'],

                str(''.join(ids[count].split(' '))), # author_id            

                ' '.join(autores[count].split(' ')), # author_name

                str((by_line(len(ids))[count])).replace(',', '.'), # author_byline

                str((by_line(len(ids)))).replace('.', '.').strip('[]'), #byline

                count+1, # author_position

                row['contrib_conception_and_design'],
                row['contrib_analysis_and_interpretation_of_the_data'], 
                row['contrib_drafting_of_the_article'], 
                row['contrib_critical_revision_for_important_intellectual_content'], 
                row['contrib_final_approval_of_the_article'], 
                row['contrib_statistical_expertise'], 
                row['contrib_obtaining_of_funding'], 
                row['contrib_administrative_technical_or_logistic_support'], 
                row['contrib_collection_and_assembly_of_data'], 
                row['contrib_provision_of_study_materials_or_patients'],

                row['c1'],
                row['c2'],
                row['c3'],
                row['c4'],
                row['c5'],
                row['c6'],
                row['c7'],
                row['c8'],
                row['c9'],
                row['c10'],

                contribuicao(' '.join(autores[count].split(';')), row['autores_novos'], row['c1']),  # contrib_study_concept_and_design
                contribuicao(' '.join(autores[count].split(';')), row['autores_novos'], row['c2']),  # contrib_critical_revision
                contribuicao(' '.join(autores[count].split(';')), row['autores_novos'], row['c3']),  # contrib_drafting_manuscript
                contribuicao(' '.join(autores[count].split(';')), row['autores_novos'], row['c4']),  # contrib_statistical_analysis
                contribuicao(' '.join(autores[count].split(';')), row['autores_novos'], row['c5']),  # contrib_study_supervision
                contribuicao(' '.join(autores[count].split(';')), row['autores_novos'], row['c6']),  # contrib_administrative_support
                contribuicao(' '.join(autores[count].split(';')), row['autores_novos'], row['c7']),  # contrib_obtained_funding
                contribuicao(' '.join(autores[count].split(';')), row['autores_novos'], row['c8']),  # contrib_acquisition_analysis_interpretation_data
                contribuicao(' '.join(autores[count].split(';')), row['autores_novos'], row['c9']),  # contrib_analysis_interpretation_data
                contribuicao(' '.join(autores[count].split(';')), row['autores_novos'], row['c10']), # contrib_acquisition_data
                
                contaSobrenomes(row['autores_novos']) # flag para verificação de sobrenomes duplicados
            ])
            count += 1
        count = 0
    except:
        print('Erro', ' '.join(autores[count].split(' ')), row['autores_novos'])
        
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
# In[262]:


df1.to_excel("annals_compilado.xlsx", header=True, index=False, encoding='utf-8')
print('Done!')


# In[5]:


df_byline = pd.read_excel('annals_compilado.xlsx', encoding='utf-8')
df_autores = pd.read_excel('annals_authors_8974.xlsx', encoding='utf-8')

resultado = pd.merge(df_byline, df_autores, on='author_id', how='inner')

resultado.to_excel("annals_final_8191.xlsx", header=True, index=False, encoding='utf-8')


# In[ ]:




