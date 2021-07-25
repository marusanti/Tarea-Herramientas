#Objetivo: Exportar un .tif de landquality en base a un .adf
 SETUP PREAMBLE FOR RUNNING STANDALONE SCRIPTS.
# NOT NECESSARY IF YOU ARE RUNNING THIS INSIDE THE QGIS GUI.
#Importacion de librerias
 print('preliminary setup')
 import sys
 import os

 from qgis.core import (
     QgsApplication, 
     QgsVectorLayer,
     QgsCoordinateReferenceSystem,
 )

 from qgis.analysis import QgsNativeAlgorithms

# # See https://gis.stackexchange.com/a/155852/4972 for details about the prefix 
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

# Setear carpetas de inputs a partir de objetos
mainpath = "/Users/magibbons/Desktop/Herramientas/Clase5/input"#carpeta general de inputs
outpath = "{}/_output/".format(mainpath)#carpeta para outputs pero que también guardar inputs que son outputs de código anterior

#Inputs
suitin = "{}/suit/suit/hdr.adf".format(mainpath)#archivo input

#Output
suitout = "{}/landquality.tif".format(outpath) #archivo output

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

# Definiendo WGS 84 SR
crs_wgs84 = QgsCoordinateReferenceSystem("epsg:4326")

##################################################################
# Warp (reproject)
#Reproyectar una capa raster a otro CRS, en este caso a las proyecciones
#que definimos en crs_wgs84
# note: Warp does not accept memory output
# could also specify: 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
# this will create new files in your OS temp directory (in my (Windows) case:
# /user/Appdata/Local/Temp/processing_somehashkey
print('defining projection for the suitability data')
warp_dict = {
    'DATA_TYPE': 0,
    'EXTRA': '',
    'INPUT': suitin,#base raster que indica calidad de la tierra
    'MULTITHREADING': False,
    'NODATA': None,
    'OPTIONS': '',
    'RESAMPLING': 0,#se elige metodo near para reproyeccion
    'SOURCE_CRS': None,
    'TARGET_CRS': crs_wgs84, #CRS elegido
    'TARGET_EXTENT': None,
    'TARGET_EXTENT_CRS': None,
    'TARGET_RESOLUTION': None,
    'OUTPUT': suitout #nombre del output
}
processing.run('gdal:warpreproject', warp_dict)
#En este caso la funcion processing.run usa el algorimo gdal:warpreproject 
#para reproyectar la capa raster a otro CRS 
#Utiliza los parametros definidos en warp_dict especificos para este algoritmo
#Como se menciono, los parametros son los mismos tanto para el input como el output

##################################################################
# Extract projection
#Creamos una proyeccion permanente del raster
print('extracting the projection for land suitability')
extpr_dict = {
    'INPUT': suitout, #partimos de la reproyeccion generada recien
    'PRJ_FILE_CREATE': True #pedimos que se genere el archivo .prj
}
processing.run('gdal:extractprojection', extpr_dict)

print('DONE!')
