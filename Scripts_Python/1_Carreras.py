
# Carreras
# Variables generadas: 


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
pln_es = spacy.load("es_core_news_sm")
from timeit import default_timer as timer
start = timer()


xls = pd.ExcelFile(clasificadores+'diccionario_clasificadores_v2.xlsx')
b= pd.read_csv(datos+'1_Contenido.csv', encoding='latin-1')

#b = b.sample(n=10000, random_state=1)

# FUNCIONES

def buscador_3(Entrada, D1):
    E = []
    for key, value in D1.items():
        for v in value:
            if Entrada.find(v) != -1:
                E.append(key)
    E = list(set(E))
    return E


# F3: convierte el excel a un diccionario
def diccionario(sheet_name):
    c1 = pd.read_excel(xls, sheet_name)
    D = c1.set_index('clave').T.to_dict('list')
    for key, value in D.items():
        D[key] = [x for x in value if str(x) != 'nan']
    return D


# CARRERAS --------------------------------------------------------

D1=diccionario('carrera')
b["carrera"] = b["contenido"].apply(buscador_3, args=(D1,))


# Detectar valores atípicos usando la clave
def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
    return num

def divide_list(List):
    original=List
    List = [round(truediv(x, 100), 0) for x in List]
    t=most_frequent(List)
    pos = [i for i, x in enumerate(List) if x != t]
    for i in sorted(pos, reverse=True):
        del original[i]
    return original

def divide_list_2(List):
    if List == []:
        return List
    else:
        return divide_list(List)



b["carrera_1"] = b["carrera"].apply(divide_list_2)

D1=diccionario('carrera_3')
def buscador_5(Entrada, D1):
    E = []
    for key, value in D1.items():
        for v in value:
            if v in Entrada:
                E.append(key)
    E = list(set(E))
    return E

b["carrera_2"] = b["carrera_1"].apply(buscador_5, args=(D1,))

b["carrera_collapse"] = b["carrera_2"].apply(lambda x: ", ".join(x)).str.replace(r'/d+', '')

l2 =['edu', 'art', 'csd', 'adn', 'cnm', 'tcc', 'ing', 'agr', 'sal', 'srv']

for i in l2:
    b[i] = b["carrera_collapse"].apply(lambda x: 1 if re.findall(i, x) else 0)




# ESCOLARIDAD ----------------------------------------------------------------

D1=diccionario('educacion')
b["educ"] = b["contenido"].apply(buscador_3, args=(D1,))

b["educ_collapse"] = b["educ"].apply(lambda x: ", ".join(x)).str.replace(r'/d+', '')


b["educacion"] = ""


b["total"] = b["edu"] + b["art"] + b["csd"] + b["adn"] + b["cnm"] + b["tcc"] + b["ing"] + b["agr"] + b["sal"] + b["srv"]

# convert b["total"] to numeric
b["total"] = pd.to_numeric(b["total"])
b["educacion"] = b["educacion"].where(b["total"]>=1, 3)
b["educacion"] = b["educacion"].where(b["educ_collapse"].str.find('medio') == -1, 2)
b["educacion"] = b["educacion"].where(b["educ_collapse"].str.find('basico') == -1, 1)

# if there is a digit in b["carrera_collapse"] then b["educacion"] = 3

b.drop(["educ",	"educ_collapse", "contenido", "carrera", "carrera_2", "carrera_collapse","titulo"], axis=1, inplace=True)


b.to_csv(resultados+'1_carreras_educacion.csv', index=False)


end = timer()
segundos=(end - start)
minutos=segundos/60
# print time with the leyend "minutes" after
print("Minutos transcurridos: ", minutos)



