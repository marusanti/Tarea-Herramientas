#Objetivo: Limpiamos la base de países
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

# Setear carpetas de inputs a partir de objeto
mainpath = "/Users/magibbons/Desktop/Herramientas/Clase5/input" #carpeta donde estan los inputs
outpath = "{}/_output/".format(mainpath)#carpeta para outputs pero que también guardar inputs que son outputs de código anterior

#Input
#elevation = "D:/backup_school/Research/IPUMS/_GEO/elrug/elevation/alt.bil"
#tpbasepath = "D:/backup_school/Research/worldclim/World"
#tpath = tpbasepath + "/temperature"
#ppath = tpbasepath + "/precipitation"
#temp = tpath + "/TOTtmean6090.tif"
#prec = ppath + "/TOTprec6090.tif"
#landqual = outpath + "/landquality.tif" #output de código anterior
#popd1500 = mainpath + "/HYDE/1500ad_pop/popd_1500AD.asc" #data de poblacion
#popd1990 = mainpath + "/HYDE/1990ad_pop/popd_1990AD.asc"#data de poblacion
#popd2000 = mainpath + "/HYDE/2000ad_pop/popd_2000AD.asc"#data de poblacion
countries = mainpath + "/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp" #shapefile de países

#output
outcsv = "{}/country_level_zs.csv".format(outpath) #csv

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
##################################################################
# Fix geometries
#Arreglamos la geometría

print('fixing geometries')
fixgeo_dict = {
    'INPUT': countries,
    'OUTPUT': 'memory:'
}
fix_geo = processing.run('native:fixgeometries', fixgeo_dict)['OUTPUT'] #guardamos como fix_geo

##################################################################
# Drop field(s)
#eliminamos todas las variables que no estén en el objeto keepfields
print('dropping unnecessary fields')
allfields = [field.name() for field in fix_geo.fields()]
keepfields = ['ADMIN', 'ISO_A3']
dropfields = [field for field in allfields if field not in keepfields]

drop_dict = {
    'COLUMN': dropfields,
    'INPUT': fix_geo,
    'OUTPUT': 'memory:' #primero guardamos en la memoria
}
drop_fields = processing.run('qgis:deletecolumn', drop_dict)['OUTPUT']#guardamos como drop_fields

###################################################################
# Exportar data final como csv
print('outputting the data')
#abrimos outpath que es el objeto que generamos para guardar el csv cuando seteamos directorio.
#Lo rellenamos con la informacion de drop_fields con la que trabajamos

with open(outcsv, 'w') as output_file:
    fieldnames = [field.name() for field in drop_fields.fields()]
    line = ','.join(name for name in fieldnames) + '\n'
    output_file.write(line)
    for f in drop_fields.getFeatures():
        line = ','.join(str(f[name]) for name in fieldnames) + '\n'
        output_file.write(line)
                                        
print('DONE!')
