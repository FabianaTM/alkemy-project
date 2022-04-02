![](https://media-exp1.licdn.com/dms/image/C4E1BAQEDDjuh9HQchg/company-background_10000/0/1610631110628?e=2159024400&v=beta&t=00JMFny1Y6JiSd8rpPDIfJ_6vNH6NhtCK_yban1zy3c)
## Challenge Data Analytics - Python
_____________________________

#### Objetivo
Crear un proyecto que consuma datos desde
3 fuentes distintas para popular una base de datos SQL con información cultural
sobre bibliotecas, museos y salas de cines argentinos.

#### Ejecución del programa

**1) Clon del repositorio**

Clonar el proyecto
```cmd
git clone https://github.com/FabianaTM/alkemy-project.git
```

**2) Configuración**

Copiar y renombrar el archivo `settings.template.ini` a `settings.ini`.
Completar las variables de configuración para establecer conexión a la base de datos.

**3) Instalación de dependencias**

```cmd
pip install -r requirements.txt
```

**4) Ejecución challenge**
```cmd
python src/main.py
```

#### Descripción de los archivos
- **src:** 
  - *datos.py*: proceso de adquisición de los datos desde la fuente, normalización de los mismos y creación de tablas con la información solicitada.
  - *main.py*: ejecuta programa completo, conexión a base de datos, creación de tablas en postgress desde archivo .sql y carga de datos creados por archivo datos.py.
  - *script*: contiene archivo .sql con scripts para la creación de tablas.
  - *data*: carpeta que va a almacenar las tablas descargadas desde la fuente original.
- **requirement.txt**: muestra las librerias y versiones utilizados para el desarrollo del programa.
- **settings.template.ini**: plantilla para configurar datos de conexión a base de datos.