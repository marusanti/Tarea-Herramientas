##Objetivo: Obtener áreas de todos los países

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

#Input
admin_in = "{}/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp".format(mainpath) #input de shapefile de paises

#Output
areas_out = "{}/_output/country_areas.csv".format(mainpath)#output de areas como csv

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

# defining world cylindrical equal area SR
crs_wcea = QgsCoordinateReferenceSystem('ESRI:54034')

##################################################################
# Drop field(s)
# Se quitan campos innecesarios de la base de estados
#En este caso la funcion processing.run usa el algorimo qgis:deletecolumn 
#para eliminar los campos que se detallan en dropfields. Se busca eliminar
#todos los campos excepto los mencionados en keepfields

print('dropping unnecessary fields')

# making a layer so we can get all attribute fields
worldlyr = QgsVectorLayer(admin_in, 'ogr')
allfields = [field.name() for field in worldlyr.fields()]
keepfields = ['ne_10m_adm', 'ADMIN', 'ISO_A3'] #lista de campos 
#forma para mantener los campos que no estan en keepfields ya que son los que
#queremos eliminar luego
dropfields = [field for field in allfields if field not in keepfields]

drop_dict = {
    'COLUMN': dropfields,#columnas a eliminar
    'INPUT': admin_in,#base de estados de la que partimos
    'OUTPUT': 'memory:'#guardamos en la memoria
}
countries_drop_fields = processing.run('qgis:deletecolumn', drop_dict)['OUTPUT'] #guardamos el objeto

##################################################################
# Reproject layer
print('projecting to world cylindical equal area')
reproj_dict = {
    'INPUT': countries_drop_fields,#partimos de base recien generada
    'TARGET_CRS': crs_wcea, #CRS elegida
    'OUTPUT': 'memory:' #guardamos en la memoria
}
countries_reprojected = processing.run('native:reprojectlayer', reproj_dict)['OUTPUT']#guardamos el objeto

##################################################################
# Fix geometries
#Corregimos geometrias
print('fixing geometries')
fixgeo_dict = {
    'INPUT': countries_reprojected,#partimos de base recien generada
    'OUTPUT': 'memory:'#guardamos en la memoria
}
countries_fix_geo = processing.run('native:fixgeometries', fixgeo_dict)['OUTPUT']#guardamos el objeto

##################################################################
# Field calculator, output to csv
#Calculamos el area del poligono y exportamos la base como csv
print('calculating country areas')
fcalc_dict = {
    'FIELD_LENGTH': 10,
    'FIELD_NAME': 'km2area',#nombre del nuevo campo
    'FIELD_PRECISION': 3,#especificamos 3 decimales 
    'FIELD_TYPE': 0, #especifamos tipo de campo como float
    'FORMULA': 'area($geometry)/1000000', #la formula para calcular el area del poligono
    'INPUT': countries_fix_geo,#partimos de base recien generada
    'NEW_FIELD': True,#especificamos que generamos un nuevo campo
    'OUTPUT': areas_out #guardamos como areas_out, esta especificada la ruta en la parte donde fijamos directorios
}
processing.run('qgis:fieldcalculator', fcalc_dict)

print('DONE!')


