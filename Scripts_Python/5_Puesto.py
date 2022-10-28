
# Carpeta donde está la última base OCC_2022_29_08_A
datos="C:/Users/jcmartinez/OneDrive - El Colegio de México A.C/5. Proyectos/2022/70. Habilidades/1. Datos/1.8 Base_Braulio_29082022/"

# Aquí esta el archivo de clasificadores
clasificadores="C:/Users/jcmartinez/OneDrive - El Colegio de México A.C/5. Proyectos/2022/70. Habilidades/1. Datos/1.6 Clasificación/INEGI_Clasificadores/"
# En el archivo "clasificadores.xlsx" se encuentran los clasificadores

resultados="C:/Users/jcmartinez/OneDrive - El Colegio de México A.C/5. Proyectos/2022/70. Habilidades/1. Datos/1.8 Base_Braulio_29082022/Base/"




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

pln_es = spacy.load("es_core_news_sm")

xls = pd.ExcelFile(clasificadores+'diccionario_clasificadores_v3.xlsx')
b= pd.read_csv(datos+'1_Contenido.csv', encoding='latin-1')

# Para probar solo una muestra
#b = b.sample(n=1000, random_state=1)

# select column "titulo" and id
b = b[['id','titulo']]

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

def diccionario(sheet_name):
    c1 = pd.read_excel(xls, sheet_name)
    c1 = c1.applymap(lambda s:s.lower() if type(s) == str else s)
    D = c1.set_index('clave').T.to_dict('list')
    for key, value in D.items():
        D[key] = [x for x in value if str(x) != 'nan']
    return D


def diccionario1(sheet_name):
    c1 = pd.read_excel(xls, sheet_name)
    # apply pln_es to all columns
    #c1 = c1.applymap(lambda s:pln_es(s) if type(s) == str else s)
    D = c1.set_index('clave').T.to_dict('list')
    for key, value in D.items():
        D[key] = [x for x in value if str(x) != 'nan']
    return D

def limpia(texto):
    texto = texto.lower()
    quitar=stopwords.words('spanish')
    r2 = r'[^\w\s\d]'
    texto = ' '.join([palabra for palabra in texto.split() if palabra not in quitar])
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r2, ' ', texto)
    return texto


b['titulo'] = b['titulo'].apply(limpia)


D1=diccionario('ocupacion')
b["ocup"] = b["titulo"].apply(buscador_3, args=(D1,))

# keep the just the first element of the list b["ocup"]
b["ocupacion"] = b["ocup"].apply(lambda x: x[0] if len(x) > 0 else x)


# drop the column b["ocup"]

b.drop(columns=['ocup'], axis=1, inplace=True)


b.to_csv(resultados+'5_puesto.csv', index=False, encoding='latin-1')


end = timer()
segundos=(end - start)
minutos=segundos/60
# print time with the leyend "minutes" after
print("Minutos transcurridos: ", minutos)