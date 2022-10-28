
# 0. CARGAR BASES --------------------------------------------------------

import numbers
import pandas as pd
from operator import truediv
import spacy
import nltk
import re
import os
from nltk.corpus import stopwords
import spacy
from spacy import displacy
from timeit import default_timer as timer
start = timer()
#nltk.download('stopwords') 
pln_es = spacy.load("es_core_news_sm")

xls = pd.ExcelFile(clasificadores+'diccionario_clasificadores_v2.xlsx')
b= pd.read_csv(datos+'1_Contenido.csv', encoding='latin-1')

# Para probar solo una muestra
#b = b.sample(n=100, random_state=1)




# 1. FUNCIONES  ----------------------------------------------------------


# palabra ---> clave
def buscador_3(Entrada, D1):
    E = []
    for key, value in D1.items():
        for v in value:
            if Entrada.find(v) != -1:
                E.append(key)
    E = list(set(E))
    return E

# palabra ---> palabra
def buscador_4(Entrada, D1):
    E = []
    for key, value in D1.items():
        for v in value:
            if Entrada.find(v) != -1:
                E.append(v)
    E = list(set(E))
    return E

# F3: convierte el excel a un diccionario
def diccionario(sheet_name):
    c1 = pd.read_excel(xls, sheet_name)
    D = c1.set_index('clave').T.to_dict('list')
    for key, value in D.items():
        D[key] = [x for x in value if str(x) != 'nan']
    return D

def limpia(texto):
    quitar=stopwords.words('spanish')
    r2 = r'[^\w\s\d]'
    texto = ' '.join([palabra for palabra in texto.split() if palabra not in quitar])
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r2, ' ', texto)
    texto = texto.lower()
    return texto


b['contenido'] = b['contenido'].apply(lambda x: limpia(x))

# vamos de regreso

def edad1(t):
    doc = pln_es(t)
    y=[]
    no_considerar=["innovación", "mercado", "trayectoria", "experiencia", "hace más de","revolucionando", "con mas de","soluciones","historia"]
    for token in doc:
        if token.pos_ == "NUM" and len(token.text) == 2 and (token.head.text=="edad" or token.head.text=="años"):
            # append the word three words before and after token.pos_
            t=doc[token.i-4:token.i+4]
            t2=t.text.split()
            if any(word in t2 for word in no_considerar):
                t2=[]
            else:
                y.append(t)
        # drop duplicates in y
        y = list(dict.fromkeys(y))
    return y             
        
def edad2(t):
    doc = pln_es(t)
    y=[]
    no_considerar=["mercado", "trayectoria", "experiencia", "hace más de","revolucionando", "con mas de","soluciones","historia"]
    for token in doc:
        if token.pos_ == "NUM" and len(token.text) == 2 and (token.head.text=="edad" or token.head.text=="años"):
            # append the word three words before and after token.pos_
            t=doc[token.i-4:token.i+4]
            t2=t.text.split()
            if any(word in t2 for word in no_considerar):
                t2=[]
            else:
                y.append(token.text)
    return y          
           
# function to extract numbers from text and delete duplicates



#b['edad1'] = b['contenido'].apply(limpia).apply(edad1)
b['edad2'] = b['contenido'].apply(limpia).apply(edad2)


# function to extract numbers from b['edad2'] and check if it is greater than 18
def edad3(t):
    y=[]
    for i in t:
        if int(i) > 18:
            y.append(i)
    return y

b['edad3'] = b['edad2'].apply(edad3)

# function to extract min b['edad3'] 
def minimo(t):
    y=[]
    for i in t:
        y.append(min(t))
    # drop duplicates in y
    y = list(dict.fromkeys(y))
    # convert y to numeric
    y = pd.to_numeric(y)
    return y

def maximo(t):
    y=[]
    for i in t:
        y.append(max(t))
    y = list(dict.fromkeys(y))
    y = pd.to_numeric(y)
    return y


b['edad_min'] = b['edad3'].apply(minimo)
b['edad_max'] = b['edad3'].apply(maximo)

b.drop(["edad2","edad3","contenido", "titulo"], axis=1, inplace=True)


b.to_csv(resultados+'4_edad.csv', index=False, encoding='latin-1')


end = timer()
segundos=(end - start)
minutos=segundos/60
# print time with the leyend "minutes" after
print("Minutos transcurridos: ", minutos)


