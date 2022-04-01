import logging
from sqlalchemy import create_engine
import psycopg2
from datos import culturaMain, registros, salas_cines
from decouple import config

logging.basicConfig(level=logging.INFO , format='%(asctime)s: %(levelname)s - %(message)s')

logging.info('Conectando a base de datos')

DATABASE_NAME = config('DATABASE_NAME',default=False)
DATABASE_USERNAME = config ('DATABASE_USERNAME',default=False)
DATABASE_PASSWORD = config ('DATABASE_PASSWORD',default=False)

db_name = DATABASE_NAME if DATABASE_NAME else input('Database: ')
user = DATABASE_USERNAME if DATABASE_USERNAME else input('Username: ')
password = DATABASE_PASSWORD if DATABASE_PASSWORD else input('Password: ')

engine=create_engine('postgresql+psycopg2://'+user+':'+password+'@localhost:5432/'+db_name)
conn= engine.connect()

logging.info('Creando tablas en base de datos')
with open('./src/script/tablas.sql', 'r') as myfile:
    data = myfile.read()
conn.execute(data)

logging.info('Cargando información a la base de datos')

#Cargar datos a las tablas creadas en postgres
salas_cines.to_sql('salas_de_cine', con=engine, if_exists='replace')
registros.to_sql('registros', con=engine, if_exists='replace')
culturaMain.to_sql('cultura', con=engine, if_exists='replace')

conn.close()

logging.info('Fin de proceso')