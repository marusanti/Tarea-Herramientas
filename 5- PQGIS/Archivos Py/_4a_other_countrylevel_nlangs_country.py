##Objetivo: Cuantificar número de lenguajes por país

#Importacion de librerias
print('preliminary setup')
import sys
import os

from qgis.core import (
     QgsApplication
 )

 from qgis.analysis import QgsNativeAlgorithms
 
#Ruta de la ubicacion de qgis 
 QgsApplication.setPrefixPath('C:/OSGeo4W64/apps/qgis', True)
 qgs = QgsApplication([], False)
 qgs.initQgis()

#Ruta del marco de procesamiento
sys.path.append('C:/OSGeo4W64/apps/qgis/python/plugins')

# Importar e iniciar marco de procesamiento
import processing
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
#########################################################################################

# Setear carpetas de inputs a partir de objeto
mainpath = "/Users/magibbons/Desktop/Herramientas/Clase5/input" #carpeta donde estan los inputs
outpath = "{}/_output/".format(mainpath)#carpeta para outputs pero que también guardar inputs que son outputs de código anterior

#Input
admin = "{}/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp".format(mainpath) #shapefile de países 
#greg = "{}/greg_cleaned.shp".format(outpath) # no utilizado
wlds = "{}/wlds_cleaned.shp".format(outpath) #es un output de codigo anterior (lenguajes)

# Output
outcsv = "{}/nlangs_country.csv".format(outpath) #archivo csv final

#A continuacion veremos que muchas de las operaciones que hacemos se realizan a 
#traves de la funcion processing.run(). Es una funcion cuyo primer parametro 
#indica el nombre del algoritmo que se quiere utilizar y el segundo indica sus
#parametros. Para especificar los parametros se usa un diccionario.
#Cada algoritmo tiene determinados parametros, aunque algunos se repiten
#en varios casos. Por ejemplo, el parametro INPUT donde se especifica el 
#archivo de origen para realizar las operaciones. El parametro output especifica
#el archivo de salida. No siempre vamos a guardarlo sino que a veces se coloca
#'memory' para que quede guardado en la memoria de la computadora y podamos 
#usarlo para otros procesos.
#En nuestros casos, como se utilizan los mismos parametros para el algoritmo
# inicial y final se coloca ['OUTPUT']. Si se usaran distintos parametros 
#habria que colocar 2 diccionarios con los parametros

#########################################################
# Fix geometries
#Corregimos la geometria del shapefile de lenguajes
print('fixing geometries, languages')
fg1_dict = {
    'INPUT': wlds,
    'OUTPUT': 'memory:'
}
fixgeo_wlds = processing.run('native:fixgeometries', fg1_dict)['OUTPUT'] #output

#Corregimos la geometria del shapefile de países 
print('fixing geometries, countries')
fg2_dict = {
    'INPUT': admin,
    'OUTPUT': 'memory:'
}
fixgeo_countries = processing.run('native:fixgeometries', fg2_dict)['OUTPUT'] #output

# Intersection
#Juntamos la base de lenguajes con el shapefile de países
print('intersecting')
int_dict = {
    'INPUT': fixgeo_wlds,
    'INPUT_FIELDS': 'GID', #variable para mergear en fix_geo_wlds
    'OVERLAY': fixgeo_countries,
    'OVERLAY_FIELDS': 'ADMIN', #variable para mergear en fix_geo_countries
    'OUTPUT': 'memory:'
}
intersection = processing.run('native:intersection', int_dict)['OUTPUT'] #output del merge


# Statistics by categories
# Contamos la cantidad de idiomas por países (variable FIELD)
print('statistics by categories')        
sbc_dict = {
    'CATEGORIES_FIELD_NAME': 'ADMIN', #variable para contar
    'INPUT': intersection,
    'VALUES_FIELD_NAME': None,
    'OUTPUT': outcsv #output final
}
processing.run('qgis:statisticsbycategories', sbc_dict)

print('DONE!')
