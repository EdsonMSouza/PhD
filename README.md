# Códigos desenvolvidos ao longo da tese de doutorado

**Título**: Aplicação de Ciência de Dados na Análise do Posicionamento Autoral e Contribuições Científicas em Artigos

**Autor**: Edson Melo de Souza, Me.

**Local**: São Paulo, junho de 2021

# Descrição dos Códigos
+ Bots - *Scripts* de extração e tratamento de dados de artigos e autores
    + annals.py - artigos do periódico Annals
    + jama.py - artigos do periódico JAMA
    + plos.py - artigos do periódico PLoS
    + authors.py - dados de autores via API Elsevier (Scopus)
    + parser.py - conversão dos dados extraídos do Scopus

+ Contribution - *Scripts* para extração e procesamento das **contribuições** dos autores
    + annals.py - contribuições do Annals
    + jama.py - contribuições do JAMA
    + plos.py - contribuições do PLoS
    + doctor.py - realiza a contagem e validação das contribuições

+ Dataclean - *Script* para tratamento e limpeza de dados obtidos do SCImago
    + dataclean.py

+ Division - *Script* para extração e divisão de autores obtidos do SCImago
    + authors_split.py

## Dependências
```bash
pip install -r requirements.txt
```

* <code>pandas==0.25.0</code>

* <code>pandas-datareader==0.7.4</code>

* <code>matplotlib==3.1.1</code>

* <code>seaborn==0.9.0</code>

* <code>selenium==3.141.0</code>

* <code>beautifulsoup4==4.8.0</code>

* <code>numpy==1.16.4</code>

* <code>openpyxl==2.6.2</code>

* <code>requests==2.22.0</code>

* <code>pathlib==1.0.1</code>

## Download do Chrome Driver
Os *scripts* são baseados no sistema operacional Windows 10. Para outros sistemas, acessar o link abaixo.  
Chrome Driver: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
