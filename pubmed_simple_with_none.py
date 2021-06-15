import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm

cit_in_cit_in_1=pd.read_csv(r'set_Journal_cit_in_cit_in_corona.csv')
a=list(cit_in_cit_in_1[pd.isna(cit_in_cit_in_1['Journal Title'])]['pmid'].values)
b=np.array_split(a, 238)

#GIUSTOOOOOOOOOOO

import time
lista=[]
for i in tqdm(range(len(b))):
    string=','.join([str(item) for item in b[i]])
    req=requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='+string+'&retmode=xml&api_key=9e46fd369b5d9d7448103ed7d418cc319a08')
    soup=BeautifulSoup(req.content, 'lxml')
    for k in range(len(soup.findAll('pubmedarticle'))):
        pmid=np.nan
        if soup.findAll('pubmedarticle')[k].find('pmid') is not None:
            pmid=soup.findAll('pubmedarticle')[k].find('pmid').get_text()
        journal_title=np.nan
        if soup.findAll('pubmedarticle')[k].find('title') is not None:
            journal_title=soup.findAll('pubmedarticle')[k].find('title').get_text()
        journal_issn=np.nan
        if soup.findAll('pubmedarticle')[k].find('issn') is not None:
            journal_issn=soup.findAll('pubmedarticle')[k].find('issn').get_text()
        affiliation=np.nan
        lista_affiliation=[]
        for j in soup.findAll('pubmedarticle')[k].findAll('affiliation'):
            lista_affiliation.append(j.get_text())
    stringhina=';'.join([str(item) for item in lista_affiliation])
    lista.append(pd.DataFrame([pmid,journal_title,journal_issn,stringhina], dtype="string").T)
    if i==237:
        print(len(lista))
    
        
