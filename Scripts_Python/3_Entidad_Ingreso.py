

# 0. CARGAR BASES --------------------------------------------------------

import pandas as pd
from operator import truediv
import spacy
import nltk
import re
import os
from timeit import default_timer as timer
start = timer()

xls = pd.ExcelFile(clasificadores+'diccionario_clasificadores_v2.xlsx')
b= pd.read_csv(datos+'1_Contenido.csv', encoding='latin-1')

#b = b.sample(n=10000, random_state=1)

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


# 7. ENTIDAD -------------------------------------------------------------


# lower case contenido
b['contenido'] = b['contenido'].str.lower()

def diccionario(sheet_name):
    c1 = pd.read_excel(xls, sheet_name)
    # convert all c1 to lower case
    c1 = c1.applymap(lambda s:s.lower() if type(s) == str else s)

    D = c1.set_index('clave').T.to_dict('list')
    for key, value in D.items():
        D[key] = [x for x in value if str(x) != 'nan']
    return D


D1=diccionario('municipio')
b["municipio"] = b["contenido"].apply(buscador_3, args=(D1,))

D1=diccionario('entidad')
b["entidad"] = b["contenido"].apply(buscador_3, args=(D1,))


# extract for position 2 to 4 of each word in "municipio" column
b['municipio_1'] = b['municipio'].apply(lambda x: [i[2:4] for i in x])

# convert each value in "municipio_1" column to numeric
b['municipio_1'] = b['municipio_1'].apply(lambda x: [int(i) for i in x])


# if some value in 'municipio_1' matches with some value of 'entidad' then return the value matched
def match_entidad(municipio, entidad):
    if municipio:
        for i in municipio:
            if i in entidad:
                return i
    else:
        return 0    

# apply match_entidad function to the 'municipio_1' and 'entidad' columns and create a new column called 'entidad_1'
b['cve_entidad'] = b.apply(lambda x: match_entidad(x['entidad'], x['municipio_1']), axis=1)


# 8. INGRESOS ------------------------------------------------------------



# regex function to extract money ranges and single values
def regex_money(text):
    # regex to extract money ranges
    money_range = re.findall(r'\$\s?\d+\s?-\s?\d+', text)
    if money_range:
        return money_range
    else:
        money_single = re.findall(r'\$\s?\d+', text)
        if money_single:
            return money_single
        else:
            return 0

# drop sign $ and values less than 1000
def clean_money(money):
    if money:
        money = [i.replace('$', '') for i in money]
        money = [i.replace(',', '') for i in money]
        money = [i.split('-') for i in money]
        money = [i for i in money if int(i[0]) > 1000]
        return money
    else:
        return 0

# average of money_2
def average_money(money):
    if money:
        money = [int(i[0]) for i in money]
        return sum(money)/len(money)
    else:
        return 0


b['prom_ingreso'] = b['contenido'].apply(regex_money).apply(clean_money).apply(average_money)
b.drop(["municipio","entidad","municipio_1","contenido", "titulo"], axis=1, inplace=True)

b.to_csv(resultados+'3_entidad_ingresos.csv', index=False, encoding='latin-1')


end = timer()
segundos=(end - start)
minutos=segundos/60
# print time with the leyend "minutes" after
print("Minutos transcurridos: ", minutos)


