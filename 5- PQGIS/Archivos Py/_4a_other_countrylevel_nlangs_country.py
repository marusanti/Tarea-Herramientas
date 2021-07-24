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

# Setear carpetas de inputs

mainpath = "/Users/magibbons/Desktop/Herramientas/Clase5/input" 
outpath = "{}/_output/".format(mainpath)

# Inputs. Los mainpath son de archivos de input data, mientras que los de outpath son outputs de códigos anteriores

admin = "{}/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp".format(mainpath) #shapefile de países 
greg = "{}/greg_cleaned.shp".format(outpath) # 
wlds = "{}/wlds_cleaned.shp".format(outpath) #

# Output

outcsv = "{}/nlangs_country.csv".format(outpath) #archivo csv final

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
#Nos quedamos con los países que tienen idiomas
print('intersecting')
int_dict = {
    'INPUT': fixgeo_wlds,
    'INPUT_FIELDS': 'GID',
    'OVERLAY': fixgeo_countries,
    'OVERLAY_FIELDS': 'ADMIN',
    'OUTPUT': 'memory:'
}
intersection = processing.run('native:intersection', int_dict)['OUTPUT'] #output


# Statistics by categories
# Contamos la cantidad de idiomas por países
print('statistics by categories')        
sbc_dict = {
    'CATEGORIES_FIELD_NAME': 'ADMIN',
    'INPUT': intersection,
    'VALUES_FIELD_NAME': None,
    'OUTPUT': outcsv #output final
}
processing.run('qgis:statisticsbycategories', sbc_dict)

print('DONE!')
