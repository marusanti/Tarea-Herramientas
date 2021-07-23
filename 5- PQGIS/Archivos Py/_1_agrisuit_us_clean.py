##Objetivo: construir un mapa que muestre la idoneidad agricola media de los 
#condados de EEUU

#Importacion de librerias
print('preliminary setup')
import sys
import os
import qgis

from qgis.core import (
    QgsApplication, 
    QgsCoordinateReferenceSystem,
)

from qgis.analysis import QgsNativeAlgorithms

# Ver https://gis.stackexchange.com/a/155852/4972 para detalles del prefijo 
#Ruta de la ubicacion de qgis 
QgsApplication.setPrefixPath('C:/OSGeo4W64/apps/qgis', True)
#Seteamos falso
qgs = QgsApplication([], False)
qgs.initQgis()

#Ruta del marco de procesamiento
sys.path.append('C:/OSGeo4W64/apps/qgis/python/plugins')

# Importar e iniciar marco de procesamiento
import processing
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
##################################################################
##################################################################

# Setear rutas de inputs and outputs
#OS module en Python provee funciones para interactuar con el sistema operativo
#Se utiliza un condicional para que si no existe la ruta descripta, se cree una
# NOTA: si se corre el script directo desde la linea de comando, se puede especificar
#rutas relativas, e.g. mainpath = "../gis_data", pero no funciona con la consola
#de python en QGIS
mainpath = "/Users/magibbons/Desktop/Herramientas/Clase5/input"
suitin = "{}/suit/suit/hdr.adf".format(mainpath)
adm2in = "{}/USA_adm_shp/USA_adm2.shp".format(mainpath)
outpath = "{}/_output/counties_agrisuit.csv".format(mainpath)
junkpath = "{}/_output/junk".format(mainpath)
junkfile = "{}/_output/junk/agrisuit.tif".format(mainpath)
if not os.path.exists(mainpath + "/_output"):
    os.mkdir(mainpath + "/_output")
if not os.path.exists(junkpath): #os.path.exists sirve para chequear si la ruta existe o no
    os.mkdir(junkpath) #mkdir sirve para crear directorio

##################################################################
##################################################################
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
#Objetos de Coordinate reference system (CRS) definen una proyeccion espeifica
# de mapa, como tambien transformaciones entre diferentes CRS
crs_wgs84 = QgsCoordinateReferenceSystem("epsg:4326")
##################################################################
###################### Warp (reproject)###########################
#Reproyectar una capa raster a otro CRS, en este caso a las proyecciones
#que definimos en crs_wgs84
##################################################################
# note: Warp does not accept memory output
# could also specify: 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
# this will create new files in your OS temp directory (in my (Windows) case:
# /user/Appdata/Local/Temp/processing_somehashkey
print('defining projection for the suitability data')
alg_params = {
    'DATA_TYPE': 0,
    'EXTRA': '',
    'INPUT': suitin, #archivo raster del que partimos
    'MULTITHREADING': False,
    'NODATA': None,
    'OPTIONS': '',
    'RESAMPLING': 0,#se elige metodo near para reproyeccion
    'SOURCE_CRS': None,
    'TARGET_CRS': crs_wgs84,#CRS 
    'TARGET_EXTENT': None,
    'TARGET_EXTENT_CRS': None,
    'TARGET_RESOLUTION': None,
    'OUTPUT': junkfile #guardamos el archivo con el nombre junkfile
}
suit_proj = processing.run('gdal:warpreproject', alg_params)['OUTPUT']
#En este caso la funcion processing.run usa el algorimo gdal:warpreproject 
#para reproyectar la capa raster a otro CRS 
#Utiliza los parametros definidos en alg_params especificos para este algoritmo
#Como se menciono, los parametros son los mismos tanto para el input como el output

##################################################################
#######################Drop fields################################
# Se quitan campos innecesarios de la base de estados
#En este caso la funcion processing.run usa el algorimo qgis:deletecolumn 
#para eliminar los campos que se detallan en alg_params.
#La lista de campos a eliminar se detalla entre [] Por ejemplo ISO, ID_O
#El imput es adm2in ya que refiere a la ruta de la base de estados
##################################################################
print('dropping fields from the county data')
alg_params = {
    'COLUMN': [' ISO','ID_0','NAME_0','ID_1','ID_2',
               'HASC_2','CCN_2','CCA_2','TYPE_2',
               'ENGTYPE_2','NL_NAME_2','VARNAME_2'],#columnas a eliminar
    'INPUT': adm2in,#base de la que partimos
    'OUTPUT': 'memory:'#guardamos en la memoria
}
counties_fields_dropped = processing.run('qgis:deletecolumn', alg_params)['OUTPUT']

###################################################################
##################Add autoincremental field########################
# Se agrega un campo cid que sera un numero que identifique al estado
#En este caso la funcion processing.run usa el algorimo native:addautoincrementalfield
#para agregar el campo cid. El input es la salida anterior (counties_fields_dropped)
###################################################################
print('adding unique ID to county data')
alg_params = {
    'FIELD_NAME': 'cid', #nombre del nuevo campo
    'GROUP_FIELDS': [''],#esto sirve para agrupar por algun campo. En este caso no agrupamos
    'INPUT': counties_fields_dropped, #base de la que partimos
    'SORT_ASCENDING': True, #orden ascendente
    'SORT_EXPRESSION': '',
    'SORT_NULLS_FIRST': False,#indicamos que no ordenamos los valores nulos
    'START': 1, #indica que se empiece a contar a partir del numero 1
    'OUTPUT': 'memory:'
}
counties_fields_autoid = processing.run('native:addautoincrementalfield', alg_params)['OUTPUT']

###################################################################
#######################Zonal statistics############################
# Se calcula la media de la idoneidad agricola por estado
#Nota: la media se calcula a partir de los pixeles del raster que se encuentran
#dentro de los estados
#En este caso la funcion processing.run usa el algorimo ative:zonalstatistics
# que sirve para hacer calculos por zona
#El input es suit_proj que es la base reproyectada que creamos
###################################################################
print('computing zonal stats')
alg_params = {
    'COLUMN_PREFIX': '_',#prefijo para el nombre de la nueva columna
    'INPUT_RASTER': suit_proj,#raster del que partimos
    'INPUT_VECTOR': counties_fields_autoid,#ultima base estados generada
    'RASTER_BAND': 1,
    'STATISTICS': 2 #2 indica que la operacion es la media
}
processing.run('native:zonalstatistics', alg_params)

###################################################################
# Exportar data final como csv
###################################################################
print('outputting the data')

with open(outpath, 'w') as output_file:
    fieldnames = [field.name() for field in counties_fields_autoid.fields()]
    line = ','.join(name for name in fieldnames) + '\n'
    output_file.write(line)
    for f in counties_fields_autoid.getFeatures():
        line = ','.join(str(f[name]) for name in fieldnames) + '\n'
        output_file.write(line)

print('DONE!')
