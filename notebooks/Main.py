
import pandas as pd
import requests
import numpy as np
import os
import geopandas as gpd
from shapely.geometry import Point
import csv
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    "--ejecucion",
    dest = "ejecucion",
    default = "MasCercana",
    help = "parametro para selecionar el tipo de ejecucion. Posibles valores: MasCercana , TodasEstaciones"
)
args = parser.parse_args(sys.argv[1:])

#DEFINO LAS FUNCIONES:
def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(float(lat), float(long))], crs=4326)
    c = c.to_crs(3857)
    return c

def distance_meters(Start, final):
    # return the distance in metres between to latitude/longitude pair point in degrees (i.e.: 40.392436 / -3.6994487)
    return Start.distance(final)

def bicimad_mas_cercana():
    i = str(input("Introduzca lugar para calcular la estacion de bicimad mas cercana: "))
    a = df_merge[df_merge["Place of interest"] == i]
    return a.sort_values(by = "Distance", ascending = True).head(1)

def tabla_bicimad_cercana():
    i = str(input("Introduzca lugar para calcular las estaciones de bicimad mas cercanas: "))
    a = df_merge[df_merge["Place of interest"] == i]
    return a.sort_values(by = "Distance", ascending = True)

# Llamo a la API para obtener los templos católicos, lo transformo en un df los depuro y los renombro, y añado una columna para identificar el tipo
templos_catolicos = requests.get('https://datos.madrid.es/egob/catalogo/209426-0-templos-catolicas.json')
templos_catolicos = templos_catolicos.json()
df1 = pd.json_normalize(templos_catolicos['@graph'])
df1 = pd.json_normalize(templos_catolicos['@graph'])
df1 = df1.drop(['@id', '@type', 'id', 'relation', 'address.district.@id', 'address.area.@id', 'address.postal-code', 'organization.organization-desc', 'organization.accesibility', 'organization.schedule', 'organization.services', 'organization.organization-name'], axis=1)
df1 = df1.rename(columns={'title':'Place of interest', 'address.locality':'City', 'address.street-address':'Place address', 'location.latitude':'lat_start', 'location.longitude':'long_start'})
df1["Type of place"] = "catolicas"

# Llamo a la API para obtener los templos no católicos, los trasnformo en un df los depuro y renombro y añado una columna para identificar el tipo
templos_no_catolicos = requests.get('https://datos.madrid.es/egob/catalogo/209434-0-templos-otros.json')
templos_no_catolicos = templos_no_catolicos.json()
df2 = pd.json_normalize(templos_no_catolicos['@graph'])
df2 = df2.drop(['@id', '@type', 'id', 'relation', 'address.district.@id', 'address.area.@id', 'address.postal-code', 'organization.organization-desc', 'organization.accesibility', 'organization.schedule', 'organization.services', 'organization.organization-name'], axis=1)
df2 = df2.rename(columns={'title':'Place of interest', 'address.locality':'City', 'address.street-address':'Place address', 'location.latitude':'lat_start', 'location.longitude':'long_start'})
df2["Type of place"] = "no_catolicas"

#Junto mis dos database en uno
frames = [df1, df2]
df_origen = pd.concat(frames)

#Ahora llamo a bicimad en mi escritorio y lo convierto en un df, lo depuro y lo renombro
df3 = pd.read_json("../data/bicimad_station.json")
df3 ['LONGITUD'] = [float(index.split(',')[0].replace("[", "")) for index in df3['geometry_coordinates']]
df3 ['LATITUD'] = [float(index.split(',')[1].replace("]", "")) for index in df3['geometry_coordinates']]
df_bicimad = df3.drop(['id', 'light', 'number', 'activate', 'no_available', 'total_bases', 'dock_bikes', 'free_bases', 'reservations_count', 'geometry_type'], axis=1)
df_bicimad = df3.rename(columns={'name': 'BiciMAD station', 'address': 'Station location', 'LONGITUD':'long_finish', 'LATITUD':'lat_finish'})

#Aplico la función to mercator al df_origen (templos catolicos y no catolicos) para convertir la latitud y la longitud en un punto
df_origen ['Start'] = df_origen.apply(lambda x: to_mercator(x['lat_start'], x['long_start']), axis =1)

#Aplico la función to mercator al df_bicimad para obtener un punto concreto en vez de latitud y longitud
df_bicimad ['final'] = df_bicimad.apply(lambda x: to_mercator(x['lat_finish'], x['long_finish']), axis =1)

#Ahora voy a crear un df juntando las dos tablas con un merge y le aplico la función distance
df_merge = pd.merge(df_origen, df_bicimad, how = 'cross')
df_merge["Distance"] = df_merge.apply(lambda x: distance_meters(x['Start'], x['final']), axis =1)

#por último voy a meter el if para que me funcione en la consola
if args.ejecucion == "MasCercana":
    ubicacion_mas_cercana = bicimad_mas_cercana()
    ubicacion_mas_cercana.to_csv("../output/ubicacion_mas_cercana.csv", sep= ";")
    print("archivo estacion mas cercana guardado en la carpeta de output")
elif args.ejecucion == "TodasEstaciones":
    todas_ubicaciones = tabla_bicimad_cercana()
    todas_ubicaciones.to_csv("../output/todas_las_ubicaciones.csv", sep= ";")
    print("archivo de todas las estaciones guardado en la carpeta de output")
else:
    print("opcion erronea, solo podemos meter: MasCercana o TodasEstaciones")
