
# Carpeta donde está la última base OCC_2022_29_08_A
datos="C:/Users/Ciencias de Datos-2/OneDrive - El Colegio de México A.C/5. Proyectos/2022/70. Habilidades/1. Datos/1.8 Base_Braulio_29082022/"

# Aquí esta el archivo de clasificadores
clasificadores="C:/Users/Ciencias de Datos-2/OneDrive - El Colegio de México A.C/5. Proyectos/2022/70. Habilidades/1. Datos/1.6 Clasificación/INEGI_Clasificadores/"
# En el archivo "clasificadores.xlsx" se encuentran los clasificadores


resultados="C:/Users/Ciencias de Datos-2/OneDrive - El Colegio de México A.C/5. Proyectos/2022/70. Habilidades/1. Datos/1.8 Base_Braulio_29082022/Base/"



# 0. CARGAR BASES --------------------------------------------------------

import pandas as pd
from operator import truediv
import spacy
import nltk
import re
import os
import warnings
warnings.filterwarnings('ignore')
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



# 2. HABILIDADES 1: crear 5 grupos  --------------------------------------


D1=diccionario('habilidade_1')

b["hab_1"] = b["contenido"].apply(buscador_3, args=(D1,))
b["hab_1n"] = b["hab_1"].apply(lambda x: ", ".join(x)).str.replace(r'/d+', '')

#l =['cognitivas', 'sociales', 'técnicas', 'personalidad', 'empresariales']
l =['cognitivas', 'sociales', 'técnicas', 'personalidad', 'empresariales', 'experiencia']

for r in l:
    b[r] = b["hab_1n"].apply(lambda x: 1 if re.findall(r, x) else 0)



# 3. HABILIDADES 2: codigos de habilidades  ------------------------------

D1=diccionario('habilidades_2')
b["hab_2"] = b["contenido"].apply(buscador_3, args=(D1,))

# convert b["habilidades_2"] into a single string
b["hab_2n"] = b["hab_2"].apply(lambda x: ", ".join(x)).str.replace(r'/d+', '')

# count the number of times "c" appears in b["habilidades_string"] 
b["cognitivas_n"] = b["hab_2n"].apply(lambda x: x.count("c"))
b["empresariales_n"] = b["hab_2n"].apply(lambda x: x.count("e"))
b["personalidad_n"] = b["hab_2n"].apply(lambda x: x.count("p"))
b["sociales_n"] = b["hab_2n"].apply(lambda x: x.count("s"))
b["tecnicas_n"] = b["hab_2n"].apply(lambda x: x.count("t"))

b["experiencia_n"] = b["hab_2n"].apply(lambda x: x.count("x"))

# sum the value of cognitivas_n	empresariales_n	personalidad_n	sociales_n	tecnicas_n
b["total_n"] = b["cognitivas_n"] + b["empresariales_n"] + b["personalidad_n"] + b["sociales_n"] + b["tecnicas_n"]+b["experiencia_n"]


# 4. HABILIDADES 2: palabras encontradas en cada habilidad  ------------------------------

D1=diccionario('habilidades_2')
b["hab_3"] = b["contenido"].apply(buscador_4, args=(D1,))

hab = pd.read_excel(xls, 'habilidades_2')
# select column opcion_1
hab = hab['opcion_1']

# for each row in hab, find the number of times it appears in b["habilidades_3"]
# not show warnings in a loop

for r in hab:
    b[r] = b["hab_3"].apply(lambda x: x.count(r))

# move position of column hab_3

b["hab_3n"] = b["hab_3"].apply(lambda x: ", ".join(x)).str.replace(r'/d+', '')

# 6. SEXO ----------------------------------------------------------------

D1=diccionario('sexo')
b["sexo"] = b["contenido"].apply(buscador_3, args=(D1,))



b.drop(["contenido","titulo", "hab_3", "hab_2","hab_1" ], axis=1, inplace=True)




# 10. SCIAN ----------------------------------------------------------------

#D1=diccionario('scian')
#b["scian"] = b["contenido"].apply(buscador_3, args=(D1,))

# 10. GUARDAR BASE DE DATOS -----------------------------------------------

b.to_csv(resultados+'2_habilidades_sexo_prueba_1000.csv', index=False, encoding='latin-1')


# drop first 3 columns to create a new dataframe
#b.drop(b.columns[[0, 1, 2]], axis=1, inplace=True)


end = timer()
segundos=(end - start)
minutos=segundos/60
# print time with the leyend "minutes" after
print("Minutos transcurridos: ", minutos)