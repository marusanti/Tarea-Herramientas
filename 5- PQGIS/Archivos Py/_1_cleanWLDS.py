##Objetivo: emprolijar información sobre lenguajes
# SETUP PREAMBLE FOR RUNNING STANDALONE SCRIPTS.
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
mainpath = "/Users/magibbons/Desktop/Herramientas/Clase5/input" #carpeta donde estan los inputs
outpath = "{}/_output/".format(mainpath)#carpeta para outputs pero que también guardar inputs que son outputs de código anterior

# Inputs
wldsin = "{}/langa.shp".format(mainpath) #archivo input de nlenguajes

#Outputs
wldsout = "{}/wlds_cleaned.shp".format(outpath) #archivo output

#Se utiliza un condicional para que si no existe la ruta descripta, se cree una
# NOTA: si se corre el script directo desde la linea de comando, se puede especificar
#rutas relativas, e.g. mainpath = "../gis_data", pero no funciona con la consola
#de python en QGIS
if not os.path.exists(outpath):  #Chequeo si el directorio existe o no
	os.mkdir(outpath) #Si no existe la ruta, genero el directorio
#OS module en Python provee funciones para interactuar con el sistema operativo

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
#Corregimos la geometria del shapefile
print('fixing geometries')
fixgeo_dict = {
    'INPUT': wldsin, #shape file input
    'OUTPUT': 'memory:'#guardamos en la memoria el archivo generado
}
fix_geo = processing.run('native:fixgeometries', fixgeo_dict)['OUTPUT'] #output de fix geometries, guardado en base a la memoria   

#######################################################################
# Add autoincremental field
# Se agrega un campo GID que sera un numero que identifique al idioma
#En este caso la funcion processing.run usa el algorimo native:addautoincrementalfield
#para agregar el campo cid. 
print('adding autoincremental id-field')
aaicf_dict = {
    'FIELD_NAME': 'GID', #nombre del nuevo campo
    'GROUP_FIELDS': None,#esto sirve para agrupar por algun campo. En este caso no agrupamos
    'INPUT': fix_geo, #tomamos al archivo recien generado
    'SORT_ASCENDING': True,#orden ascendente
    'SORT_EXPRESSION': '',
    'SORT_NULLS_FIRST': False,#indicamos que no ordenamos los valores nulos
    'START': 1,#indica que se empiece a contar a partir del numero 1
    'OUTPUT': 'memory:'#guardamos en la memoria el archivo generado
}
autoinc_id = processing.run('native:addautoincrementalfield', aaicf_dict)['OUTPUT'] #output de fix autoincremental

#########################################################
# Field calculator
#Calculamos el largo de la variable NAME_PROP (cantidad de caracteres) y luego
#filtramos para quedarnos solo con los campos donde NAME_PROP tenga menos de
#10 caracteres
print('copying language name into a field with shorter attribute name')
fc_dict = {
    'FIELD_LENGTH': 10,#indicamos hasta 10 caracteres para el filtro
    'FIELD_NAME': 'lnm',#nombre del campo
    'FIELD_PRECISION': 0,
    'FIELD_TYPE': 2, #indicamos que el campo es string
    'FORMULA': ' attribute($currentfeature, \'NAME_PROP\')',
    'INPUT': autoinc_id,#partimos de base generada recien
    'NEW_FIELD': True,#indica que estamos generando un nuevo campo
    'OUTPUT': 'memory:'#guardamos en la memoria el archivo generado
}
field_calc = processing.run('qgis:fieldcalculator', fc_dict)['OUTPUT']  #output del field calculator

#########################################################
# Drop field(s)
# Se quitan campos innecesarios de la base recién generada
print('dropping fields except GID, ID, lnm')
#queremos eliminar todos los campos excepto los mencionados en keepfields
allfields = [field.name() for field in field_calc.fields()]
keepfields = ['GID', 'ID', 'lnm']
dropfields = [field for field in allfields if field not in keepfields]#objeto que contiene columnas a eliminar

df3_dict = {
   'COLUMN': dropfields,# eliminamos las columnas mencionadas en dropfields
   'INPUT': field_calc,#partimos de ultimo archivo generado
   'OUTPUT': wldsout #guardamos este archivo con el nombre de wldsout ya que antes definimos la ruta para el archivo con este nombre
}
processing.run('qgis:deletecolumn', df3_dict)

print('DONE!')
