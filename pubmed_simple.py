import pandas as pd 
 
import numpy as np
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import time

APYKEY='your personal apikey from pubmed' #https://www.ncbi.nlm.nih.gov/account/settings/?smsg=create_apikey_success
cit_in_cit_in_1=pd.read_csv('set_Journal_cit_in_cit_in_corona.csv')

a=list(cit_in_cit_in_1[pd.isna(cit_in_cit_in_1['Journal Title'])]['pmid'].values)
i=238
b=np.array_split(a, i)  #choose i  as number to have n arrays of length 300

string=','.join([str(item) for item in b[0]])
req=requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='+string+'&retmode=xml&api_key='+str(APIKEY))
soup=BeautifulSoup(req.content, 'lxml')
lista_pmid=[]
for j in soup.findAll('pmid'):
    lista_pmid.append(str(j).replace('<pmid version="1">','').replace('</pmid>',''))
lista_journal=[]
for k in soup.findAll('title'):
    lista_journal.append(str(k).replace('<title>','').replace('</title>',''))
pro=pd.DataFrame([lista_pmid,lista_journal]).T #create first dataframe


lista=[]
m=237 #last element
for i in tqdm(range(1,len(b))):
    string=','.join([str(item) for item in b[i]])
    req=requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='+string+'&retmode=xml&api_key=9e46fd369b5d9d7448103ed7d418cc319a08')
    soup=BeautifulSoup(req.content, 'lxml')
    lista_pmid=[]
    for j in soup.findAll('pmid'):
        lista_pmid.append(str(j).replace('<pmid version="1">','').replace('</pmid>',''))
    lista_journal=[]
    for k in soup.findAll('title'):
        lista_journal.append(str(k).replace('<title>','').replace('</title>',''))

    lista.append(pd.DataFrame([lista_pmid,lista_journal]).T)
    time.sleep(1)
    if i==m:
        print(len(lista))
    
        
