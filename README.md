<p align="left"><img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.emesa-m30.es%2Festaciones-bicimad-dentro-m-30%2F&psig=AOvVaw178f3yQFMxsyb_zVcSsjCB&ust=1642794937369000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCNCZqpeOwfUCFQAAAAAdAAAAABAD"></p>

#  Proyecto Santi Oriol -- Estación más cercana

Ironhack Madrid - Data Analytics Part Time - November 2021 - Project Module 1

## Explicación del proyecto

El proyecto consiste en crear una aplicación para obtener la estación de bicis más cercana (BiciMAD) desde el punto de interés que el usuario quiera.
Para ello, se limitan los puntos de interés a los templos religiosos tanto católicos como no católicos.

---

## Instrucciones de uso

1) Abrir la terminal "Power Shell" en el caso de windows
2) Meterse en el entorno "Proyect1_bueno" con el comando conda activate
3) Acceder a la carpeta donde se encuentra el código de la aplicación. Este archivo "main.py". Para ello se debe ejecutar el comando "cd" y añadir la siguiente ruta: \Desktop\Ironhack\ih_datamadpt1121_project_m1\notebooks>
4) Para ejecutar la aplicación se debe introducir el comando python main.py --ejecuion
5) Se puede obtener la estación más cercana añadiendo al paso 4 MasCercana o si se quieren obtener todas las estaciones de bicimad en relación al punto de interés se deberá añadir al punto 4 TodasEstaciones
6) La aplicación le dirá que introduzca el punto de interés OJO, debe ser literal
7) La aplicación le creará un fichero csv en la carpeta output

## Librerías

Para poder crear el código se han utilizado las siguientes librerías:
1) **Pandas**: Para poder trabajar en dataframes
2) **Requests**: Para conectarse a la api del ayuntamiento y obtener los puntos de interés
3) **os**: Para poder acceder a carpetas del ordenador
4) **geopandas**: Para trabajar con coordenadas y transformarlos en puntos concretos y así medir las distancias
5) **shapely.geometry**: Para medir distancias entre puntos
6) **argparse**: Para conectar el pipeline creado con la terminal
    
## Metodología seguida ETC

### Extracción ###

**Bicimad**: Se han obtenido los datos de Bicimad a través de azure data studio, guaradando el archivo en local
**Templos**: Por medio de la [API](https://datos.madrid.es/nuevoMadrid/swagger-ui-master-2.2.10/dist/index.html?url=/egobfiles/api.datos.madrid.es.json#/) del ayuntamiento de Madrid y con la librería request.

### Transformación ###
**Jupyter**
La transformación de los datos se ha realizado con el siguiente orden:
1) Se han convertido los datos en dataframes
2) Se han limpiado y renombrado 
3) Se han unido todos los datos en una sola tabla
4) Sobre esa tabla se ha aplicado la función *Distance* para calcular la distancia entre el punto de interés y la estación de bicimad
5) A continuación se han creado dos funciones para caluclar la estación de bicis más cercana *bicimad_mas_cercana* y todas las               estaciones ordenadas en función de la distancia *Tabla_bicimad_cercana*

**Visual studio code**
1) Se ha creado un archivo .py
2) Se ha realizado un pipeline con argparse para conectar con la terminal.
3) Se ha introducido el código de jupyter
4) Se ha añadido una función if que recibe los imputs del argparse y del usuario para correr las funciones deseadas en función del tipode ejecución que haya seleccionado el usuario
    
### Carga ###
**Visual studio code**
1) En el if mencionado en el paso 4 del apartado anterior, se ordena que se cree un archivo csv local en función del tipo de ejecución          que seleccione el usuario









 


 

