##Objetivo: Obtener centroides y distancias a la costa de todos los países

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

# Inputs. Los mainpath son de archivos de input data, mientras que los de outpath son outputs de códigos anteriores
coastin = "{}/ne_10m_coastline/ne_10m_coastline.shp".format(mainpath) #shapefile de costas
adminin = "{}/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp".format(mainpath) #shapefile de países

# Outputs
junkpath = "{}/junk".format(outpath) #archivos temporales
coastout = "{}/coast.shp".format(junkpath) #shapefile de costas maritimas
centroidsout = "{}/centroids.shp".format(junkpath) #shapefile de centroides de países
distout = "{}/distance.shp".format(junkpath) #shapefile de lineas verticales de centroides a la costa 
nearout = "{}/nearest.shp".format(junkpath) #shapefiles de puntos costeros más cercanos al centroide
testout = "{}/testout.shp".format(junkpath)
csvout = "{}/centroids_closest_coast.csv".format(outpath) #csv final

#OS module en Python provee funciones para interactuar con el sistema operativo
#Se utiliza un condicional para que si no existe la ruta descripta, se cree una
# NOTA: si se corre el script directo desde la linea de comando, se puede especificar
#rutas relativas, e.g. mainpath = "../gis_data", pero no funciona con la consola
#de python en QGIS

if not os.path.exists(junkpath):
    os.mkdir(junkpath)

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

# #########################################################################
# # Fix geometries
#Corregimos la geometria del shapefile de costas maritimas y lo guardamos como fixgeo_coast
 print('fixing geometries, coast')
 fg1_dict = {
     'INPUT': coastin,
     'OUTPUT': 'memory:'
 }
 fixgeo_coast = processing.run('native:fixgeometries', fg1_dict)['OUTPUT']

 #Corregimos la geometria del shapefile de países y lo guardamos como fixgeo_coutries
 print('fixing geometries, countries')
 fg2_dict = {
     'INPUT': adminin,
     'OUTPUT': 'memory:'
 }
 fixgeo_countries = processing.run('native:fixgeometries', fg2_dict)['OUTPUT']

# # Centroids
# Obtener los centroides de los países (la función devuelve el centro geográfico, 
#no las capitales nacionales) y lo guardamos como country_centroids
print('finding country centroids')
 cts_dict = {
     'ALL_PARTS': False,
     'INPUT': fixgeo_countries, #input de codigo anterior
     'OUTPUT': 'memory:'
 }
 country_centroids = processing.run('native:centroids', cts_dict)['OUTPUT']

# # Add geometry attributes
# le agregamos las coordenadas a los centroides y lo guardamos como centroids_with_coordinates   
 print('adding co-ordinates to centroids')    
 aga1_dict = {
     'CALC_METHOD': 0,
     'INPUT': country_centroids,
     'OUTPUT': 'memory:'
 }
centroids_with_coordinates = processing.run('qgis:exportaddgeometrycolumns', aga1_dict)['OUTPUT']

# # Drop field(s)
# nos quedamos solo con la información de fixgeo_coast que necesitamos y guardamos como coastout
 print('dropping unnecessary fields, coast')
 allfields = [field.name() for field in fixgeo_coast.fields()]
 keepfields = ['featurecla']#variables que no borramos
 dropfields = [field for field in allfields if field not in keepfields]

 df1_dict = {
     'COLUMN': dropfields,
     'INPUT': fixgeo_coast,
     'OUTPUT': coastout
 }
 processing.run('qgis:deletecolumn', df1_dict)

# nos quedamos solo con la información de centroids_with_coordinates que necesitamos y guardamos como centroids_out

 print('dropping unnecessary fields, countries')
 allfields = [field.name() for field in centroids_with_coordinates.fields()]
 keepfields = ['ne_10m_adm', 'ADMIN', 'ISO_A3', 'xcoord', 'ycoord']#variables que no borramos
 dropfields = [field for field in allfields if field not in keepfields]

# df2_dict = {
     'COLUMN': dropfields,
     'INPUT': centroids_with_coordinates,
     'OUTPUT': centroidsout
 }
 processing.run('qgis:deletecolumn', df2_dict)


# v.distance
#medimos la distancia de los centroides (centroidsout) a la costa (coastout) con la función v.distance
#guardamos como nearout al punto más cercano y como distout a la distancia entre ese punto y el centroide 
print('vector distance')
vd_dict = {
    'from': centroidsout, #extremo incial de la línea
    'from_type': [0],
    'to': coastout, #extremo final de la línea
    'to_type': [1],
    'dmax': -1,
    'dmin': -1,
    'upload': [1],
    'column': ['xcoord'],
    'to_column': None,
    'from_output': nearout, #nos quedamos con los puntos costeros, parte del uutput
    'output': distout,  #el output es la distancia
    'GRASS_REGION_PARAMETER': None,
    'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
    'GRASS_MIN_AREA_PARAMETER': 0.0001,
    'GRASS_OUTPUT_TYPE_PARAMETER': 0,
    'GRASS_VECTOR_DSCO': '',
    'GRASS_VECTOR_LCO': '',
    'GRASS_VECTOR_EXPORT_NOCAT': False
}
processing.run('grass7:v.distance', vd_dict)

# # Field calculator
#le restamos uno a nearout para que tengan sentido los valores
#guardamos como nearest_cat_adjust
 print('adjusting the "cat" field in the nearest centroids to merge with distance lines')
 fc1_dict = {
     'FIELD_LENGTH': 4,#largo del nombre
     'FIELD_NAME': 'cat',#nombre de la variable
     'FIELD_PRECISION': 3,#especificamos 3 decimales 
     'FIELD_TYPE': 1,#integer
     'FORMULA': 'attribute($currentfeature, \'cat\')-1',#formula de restarle 1
     'INPUT': nearout,#input
     'NEW_FIELD': False,
     'OUTPUT': 'memory:'
 }
 nearest_cat_adjust = processing.run('qgis:fieldcalculator', fc1_dict)['OUTPUT']

# # Drop field(s)
# Borramos las variables innecesarias dentro del objeto nearest_cat_adjust
 print('dropping unnecessary fields, nearest (the co-ordinates get screwed up')
 df3_dict = {
     'COLUMN': ['xcoord', 'ycoord'],#solo nos quedamos con las coordenadas
     'INPUT': nearest_cat_adjust,
     'OUTPUT': 'memory:'
 }
 nearest_cat_adjust_dropfields = processing.run('qgis:deletecolumn', df3_dict)['OUTPUT']

# # Join attributes by field value
# Mergeamos data de controides (centroidsout) con punto costero más cercano (nearest_cat_adjust)
#guardamos el join como centroids_nearest_coast_joined
print('merging the two tables: nearest and centroids: correct co-ordiantes')
jafv1_dict = {
    'DISCARD_NONMATCHING': False,
    'FIELD': 'ne_10m_adm', #variable a mergear (pais)
    'FIELDS_TO_COPY': None,
    'FIELD_2': 'ne_10m_adm', #variable a mergear (pais)
    'INPUT': centroidsout, #objeto a mergear
    'INPUT_2': nearest_cat_adjust_dropfields, #objeto a mergear
    'METHOD': 1,
    'PREFIX': '',
    'OUTPUT': 'memory:'
}
centroids_nearest_coast_joined = processing.run('native:joinattributestable', jafv1_dict)['OUTPUT']

# # Drop field(s)
# Borramos las variables innceesarias del join
 print('dropping unnecessary fields, nearest and centroids merge')
 df4_dict = {
     'COLUMN': ['ne_10m_adm_2', 'ADMIN_2', 'ISO_A3_2'],
     'INPUT': centroids_nearest_coast_joined,
     'OUTPUT': 'memory:'
 }
 centroids_nearest_coast_joined_dropfields = processing.run('qgis:deletecolumn', df4_dict)['OUTPUT']

# # Join attributes by field value
#Le agregamos al merge anterior la información de distancia
 print('merging the two tables: nearest (adjusted) and distance (this adds countries to each centroid-coast line)')
 jafv2_dict = {
     'DISCARD_NONMATCHING': False,
     'FIELD': 'cat',
     'FIELDS_TO_COPY': None,
     'FIELD_2': 'cat',
     'INPUT': distout,
     'INPUT_2': centroids_nearest_coast_joined_dropfields,
     'METHOD': 1,
     'PREFIX': '',
     'OUTPUT': 'memory:'
 }
 centroids_nearest_coast_distance_joined = processing.run('native:joinattributestable', jafv2_dict)['OUTPUT']

# # Extract vertices
# extraemos vértices de distancia para quedarnos solamente con aquellos que estén en la costa
#guardamos como objeto extract_by_attribute 
 print('extracting vertices (get endpoints of each line)')     
 ev_dict = {
     'INPUT': centroids_nearest_coast_distance_joined,
     'OUTPUT': 'memory:'
 }
 extract_vertices = processing.run('native:extractvertices', ev_dict)['OUTPUT']

 print('keeping only vertices on coast')
 eba_dict = {
     'FIELD': 'distance',#usamos la variable distancia
     'INPUT': extract_vertices,
     'OPERATOR': 2,#para extraer vertice
     'VALUE': '0',
     'OUTPUT': 'memory:'
 }
 extract_by_attribute = processing.run('native:extractbyattribute', eba_dict)['OUTPUT']

# # Field calculator
# agregamos las coordinadas del centroide
 print('creating new field: centroid latitude (keep field names straight)')
 fc2_dict = {
     'FIELD_LENGTH': 10,#largo del nombre
     'FIELD_NAME': 'cent_lat',#y_coord
     'FIELD_PRECISION': 10,#precisión
     'FIELD_TYPE': 0,#float
     'FORMULA': 'attribute($currentfeature, \'ycoord\')',#formula para obtener latitud
     'INPUT': extract_by_attribute,
     'NEW_FIELD': False,
     'OUTPUT': 'memory:'
 }
 added_field_cent_lat = processing.run('qgis:fieldcalculator', fc2_dict)['OUTPUT']

 print('creating new field: centroid longitude (keep field names straight)')
 fc3_dict = {
     'FIELD_LENGTH': 10,
     'FIELD_NAME': 'cent_lon',#x_coord
     'FIELD_PRECISION': 10,
     'FIELD_TYPE': 0,
     'FORMULA': 'attribute($currentfeature, \'xcoord\')',
     'INPUT': added_field_cent_lat,
     'NEW_FIELD': False,
     'OUTPUT': 'memory:'
 }
 added_field_cent_lon = processing.run('qgis:fieldcalculator', fc3_dict)['OUTPUT']


# # Drop field(s)
# Borrar columnas innecesarias
 print('dropping unnecessary fields')
 allfields = [field.name() for field in added_field_cent_lon.fields()]
 keepfields = ['ne_10m_adm', 'ADMIN', 'ISO_A3', 'cent_lat', 'cent_lon']#variables que quedan
 dropfields = [field for field in allfields if field not in keepfields]

 df5_dict = {
     'COLUMN': dropfields,
     'INPUT': added_field_cent_lon,
     'OUTPUT': 'memory:'
 }
 centroids_lat_lon_drop_fields = processing.run('qgis:deletecolumn', df5_dict)['OUTPUT']

# # Add geometry attributes
# Agregar coordenadas. Aplican los comentarios de pasos anteriores    
 print('adding co-ordinates to coast points')    
 aga2_dict = {
     'CALC_METHOD': 0,
     'INPUT': centroids_lat_lon_drop_fields,
     'OUTPUT': 'memory:'
 }
 add_geo_coast = processing.run('qgis:exportaddgeometrycolumns', aga2_dict)['OUTPUT']


 print('creating new field: centroid latitude (keep field names straight)')
 fc4_dict = {
     'FIELD_LENGTH': 10,
     'FIELD_NAME': 'coast_lat',
     'FIELD_PRECISION': 10,
     'FIELD_TYPE': 0,
     'FORMULA': 'attribute($currentfeature, \'ycoord\')',
     'INPUT': add_geo_coast,
     'NEW_FIELD': False,
     'OUTPUT': 'memory:'
 }
 added_field_coast_lat = processing.run('qgis:fieldcalculator', fc4_dict)['OUTPUT']

 print('creating new field: centroid longitude (keep field names straight)')
 fc5_dict = {
     'FIELD_LENGTH': 10,
     'FIELD_NAME': 'coast_lon',
     'FIELD_PRECISION': 10,
     'FIELD_TYPE': 0,
     'FORMULA': 'attribute($currentfeature, \'xcoord\')',
     'INPUT': added_field_coast_lat,
     'NEW_FIELD': False,
     'OUTPUT': 'memory:'
 }
 added_field_coast_lon = processing.run('qgis:fieldcalculator', fc5_dict)['OUTPUT']

# # Drop field(s)
# #guardar las coordenadas en el csvout
 print('dropping unnecessary fields')

 df6_dict = {
     'COLUMN': ['xcoord', 'ycoord'],
     'INPUT': added_field_coast_lon,
     'OUTPUT': csvout
 }
 processing.run('qgis:deletecolumn', df6_dict)


print('DONE!')
