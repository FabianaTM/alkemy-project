# Importar librerias necesarias para la obtención y procesamiento de datos

import pandas as pd
import io
import requests
import numpy as np
import logging
import os
from datetime import date
from datetime import datetime

ROOT_DATA_PATH = './src/data'

logging.basicConfig(level=logging.INFO , format='%(asctime)s: %(levelname)s - %(message)s')


logging.info('Obteniendo datos y generando archivos')

fecha= datetime.now().strftime('%m-%d-%Y')
anio= date.today().year
mes= datetime.now().strftime("%B")


# MUSEOS

urlmuseos= 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museo.csv'
rmuseos = requests.get(urlmuseos)

museosContenido=requests.get(urlmuseos).content
museoCSV=pd.read_csv(io.StringIO(museosContenido.decode('utf-8')))
museos=pd.DataFrame(museoCSV)



dirNameMuseos = ( ROOT_DATA_PATH + '/museos/'+str(anio)+'-'+str(mes)+'/')

# Crear directorio de destino si no existe
if not os.path.exists(dirNameMuseos):
    os.makedirs(dirNameMuseos)
    print("Directory " , dirNameMuseos ,  " Created ")
else:    
    print("Directory " , dirNameMuseos ,  " already exists")

# Guardar el archivo de formal local, si el archivo existe, lo reemplaza

ruta_museos=(str(dirNameMuseos)+'/museos-'+str(fecha)+'.csv')
print(ruta_museos)

museos.to_csv(ruta_museos,
    sep = ',',
    index= False,
    encoding= 'utf-8')


# CINES

urlCines= 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv'
rCines = requests.get(urlCines) 

CinesContenido=requests.get(urlCines).content
CinesCSV=pd.read_csv(io.StringIO(CinesContenido.decode('utf-8')))
cines=pd.DataFrame(CinesCSV)

dirNameCines = (ROOT_DATA_PATH + '/cines/'+str(anio)+'-'+str(mes)+'/')

# Crear directorio de destino si no existe
if not os.path.exists(dirNameCines):
    os.makedirs(dirNameCines)
    print("Directory " , dirNameCines ,  " Created ")
else:    
    print("Directory " , dirNameCines ,  " already exists")

ruta_cines=(str(dirNameCines)+'/cines-'+str(fecha)+'.csv')
print(ruta_cines)

cines.to_csv(ruta_cines,
    sep = ',',
    index= False,
    encoding= 'utf-8')


# BIBLIOTECAS

urlBibliotecas= 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv'
rBibliotecas = requests.get(urlBibliotecas) 

bibliotecasContenido=requests.get(urlBibliotecas).content
bibliotecasCSV=pd.read_csv(io.StringIO(bibliotecasContenido.decode('utf-8')))
bibliotecas=pd.DataFrame(bibliotecasCSV)

dirNameBibliotecas = (ROOT_DATA_PATH + '/bibliotecas/'+str(anio)+'-'+str(mes)+'/')

# Crear directorio de destino si no existe
if not os.path.exists(dirNameBibliotecas):
    os.makedirs(dirNameBibliotecas)
    print("Directory " , dirNameBibliotecas ,  " Created ")
else:    
    print("Directory " , dirNameBibliotecas ,  " already exists")

ruta_bibliotecas=(str(dirNameBibliotecas)+'/bibliotecas-'+str(fecha)+'.csv')
print(ruta_bibliotecas)

bibliotecas.to_csv(ruta_bibliotecas,
    sep = ',',
    index= False,
    encoding= 'utf-8')


# Procesamiento de datos

logging.info('Procesando datos')

# Cambiar el nombre de las columnas que tienen en común para que queden iguales

nombre_columnas={'Cod_Loc':'Cod_localidad',
                'IdProvincia':'Id_provincia',
                'IdDepartamento':'Id_departamento',
                'Observacion':'Observaciones',
                'categoria':'Categoría',
                'subcategoria':'Subcategoria',
                'provincia':'Provincia',
                'localidad':'Localidad',
                'nombre':'Nombre',
                'direccion':'Domicilio',
                'Dirección':'Domicilio',
                'piso':'Piso',
                'cod_area':'Cod_tel',
                'telefono':'Teléfono',
                'Info_adicional':'Información adicional',
                'fuente':'Fuente',
                'tipo_gestion':'Tipo_gestion',
                'año_inicio':'año_inauguracion',
                'actualizacion':'Año_actualizacion',
                'año_actualizacion':'Año_actualizacion'
                }

# Renombrar columnas de los archivos
museos= museos.rename(columns=nombre_columnas)
cines= cines.rename(columns=nombre_columnas)
bibliotecas= bibliotecas.rename(columns=nombre_columnas)

# Crear archivo unificado
cultura= pd.concat([museos,cines,bibliotecas])

# Reemplazar valores s/d correspondientes a Nan
cultura=cultura.replace('s/d',np.nan)

# Corregir nombre de provincias
cultura= cultura.replace({'Tierra del Fuego':'Tierra del Fuego, Antártida e Islas del Atlántico Sur',
                                   'Santa Fé':'Santa Fe',
                                   'Neuquén ':'Neuquén'})


# Creación de tablas

logging.info('Creando tablas')

# Tabla CulturaMain
culturaMain= cultura.loc[:,['Cod_localidad','Id_provincia', 'Id_departamento','Categoría','Provincia', 'Localidad', 'Nombre',
       'Domicilio','CP','Teléfono', 'Mail', 'Web']]

# Agregamos columna de fecha de carga
culturaMain['Fecha carga']= datetime.today().strftime('%d-%m-%Y')


# Tabla registros
tabla_registros=pd.DataFrame(cultura.groupby(['Categoría','Fuente','Provincia']).size(), columns=['Totales'])
tabla_registros.drop(['Totales'], axis=1, inplace=True)

#Creamos tablas intermedias con la información solicitada
categoria= pd.DataFrame(cultura.groupby(['Categoría']).size(),columns=['Total por categoría'])  #Cantidad de registros totales por categoría
fuente=pd.DataFrame(cultura.groupby(['Fuente']).size(),columns=['Total por fuente'])    #Cantidad de registros totales por fuente
categoria_provincia= pd.DataFrame(cultura.groupby(['Categoría','Provincia']).size(),columns=['Total categoría por provincia'])   #Cantidad de registros por provincia y categoría

#Juntar información para formación de tabla
reg_cat= tabla_registros.merge(categoria, how='inner', left_index=True, right_index=True)
reg_cat_fue=reg_cat.merge(fuente, how='inner', left_index=True, right_index=True)
tabla_registros_merge=reg_cat_fue.merge(categoria_provincia, how='inner', left_index=True, right_index=True)
registros= tabla_registros_merge.reset_index()  # Resetear index
registros['Fecha carga']= datetime.today().strftime('%d-%m-%Y') # Agregar columna de fecha de carga


#Tabla salas de cine
tabla_salas_cines =cultura[cultura.Categoría =='Salas de cine']

pantallas_butacas= tabla_salas_cines.groupby(['Provincia']).sum().round(0).astype(int).loc[:,['Pantallas', 'Butacas']]
espacio_INCAA= tabla_salas_cines.groupby(['Provincia']).count().loc[:,['espacio_INCAA']]

salas_cines=pantallas_butacas.merge(espacio_INCAA, how='inner', left_index=True, right_index=True) #unir información
salas_cines['Fecha carga']= datetime.today().strftime('%d-%m-%Y') # Agregar columna de fecha de carga
salas_cines=salas_cines.reset_index() # resetear index



logging.info('Fin de proceso normalización de datos y creación de tablas')