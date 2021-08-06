#Importacion de librerias
print('preliminary setup')
import sys
import os

#from qgis.core import (
#     QgsApplication
# )

#from qgis.analysis import QgsNativeAlgorithms
import processing
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
#########################################################################################
#########################################################################################

from geoprocess import GeoProcess

# set paths to inputs and outputs
# mainpath = "C:/Users/giorg/Dropbox (LBS Col_con)/PoliteconGIS/LBS_2020/PhD/lecture_5/gis_data"
mainpath = "/Users/matia/Documents/UDESA/7_HComp/Tarea-Herramientas/6-PQGIS_2/data"
outpath = "{}/_output/".format(mainpath)
junkpath = "{}/junk/".format(outpath)

capitales = "{}/capitales.shp".format(mainpath)
trenes = "{}/lineas_de_transporte_ferroviario_AN010.shp".format(mainpath)
#tren90 = "{}/tren1890_p.shp".format(mainpath)
ruta = "{}/_3_4_1_1_6_rutas_nacionales_dnv18_view.shp".format(mainpath)


from_centroids21 = "{}/from_centroids21.shp".format(junkpath)
distance_centroids21 = "{}/distance_centroids21.shp".format(junkpath)
#from_centroids90 = "{}/from_centroids90.shp".format(junkpath)
#distance_centroids90 = "{}/distance_centroids90.shp".format(junkpath)
t1 = "{}/_test1.shp".format(junkpath)
t2 = "{}/_test2.shp".format(junkpath)
out21 = "{}/lines_for_network_1821.shp".format(outpath)
#out90 = "{}/lines_for_network_1890.shp".format(outpath)
outcent = "{}/county_centroids.shp".format(outpath)

if not os.path.exists(junkpath):
    os.mkdir(junkpath)

gp = GeoProcess()


###########################################################################
###########################################################################
###########################################################################

######################################################################
# reproject ruta, tren, and capitales to WGS84
######################################################################
print('reprojecting ruta, tren, and capitales to WGS84')
treneswgs84 = gp.reproject_layer(trenes, 'EPSG:4326')
#tren90wgs84 = gp.reproject_layer(tren90, 'EPSG:4326')
rutawgs84 = gp.reproject_layer(ruta, 'EPSG:4326')
capitaleswgs84 = gp.reproject_layer(capitales, 'EPSG:4326')

######################################################################
# county centroids
######################################################################
print('finding county centroids')
centroids = gp.centroids(capitaleswgs84)

######################################################################
# adding indicators and dropping unnecessary fields
######################################################################
print('adding indicators')
treneswgs84 = gp.add_constant_field(treneswgs84, 'tren', 1)
#tren90wgs84 = gp.add_constant_field(tren90wgs84, 'tren', 1)
rutawgs84 = gp.add_constant_field(rutawgs84, 'ruta', 1)
centroids = gp.add_constant_field(centroids, 'centroids', 1)

print('dropping unnecessary fields')
treneswgs84 = gp.drop_fields(treneswgs84, keep_fields=['tren'])
#tren90wgs84 = gp.drop_fields(tren90wgs84, keep_fields=['tren'])
rutawgs84 = gp.drop_fields(rutawgs84, keep_fields=['ruta'])
centroids = gp.drop_fields(centroids, keep_fields=['centroids'])

######################################################################
# splitting with lines, snapping and unioning ruta and tren
######################################################################
print('splitting with lines, snapping and unioning ruta and tren')
trenes_split_ruta = gp.split_with_lines(treneswgs84, rutawgs84)
#tren90_split_ruta = gp.split_with_lines(tren90wgs84, rutawgs84)
ruta_split_trenes = gp.split_with_lines(rutawgs84, treneswgs84)
#ruta_split_tren90 = gp.split_with_lines(rutawgs84, tren90wgs84)

trenes_snap_ruta = gp.snap_geometries(trenes_split_ruta, ruta_split_trenes, 0.01)
#tren90_snap_ruta = gp.snap_geometries(tren90_split_ruta, ruta_split_tren90, 0.01)

ruta_split_trenes = gp.fix_geometry(ruta_split_trenes)
#ruta_split_tren90 = gp.fix_geometry(ruta_split_tren90)
trenes_snap_ruta = gp.fix_geometry(trenes_snap_ruta)
#tren90_snap_ruta = gp.fix_geometry(tren90_snap_ruta)

ruta_split_trenes = gp.multipart_to_singleparts(ruta_split_trenes)
#ruta_split_tren90 = gp.multipart_to_singleparts(ruta_split_tren90)
trenes_snap_ruta = gp.multipart_to_singleparts(trenes_snap_ruta)
#tren90_snap_ruta = gp.multipart_to_singleparts(tren90_snap_ruta)

union_trenruta = gp.union(ruta_split_trenes, trenes_snap_ruta)
#union_trenruta90 = gp.union(ruta_split_tren90, tren90_snap_ruta)

######################################################################
# creating connector pieces, snapping, splitting and unioning
######################################################################
print('creating connector pieces, snapping, splitting and unioning, 2021')
gp.grass_v_distance(centroids, union_trenruta, 'centroids',
                    from_out=from_centroids21, dist_out=distance_centroids21)
connectors21 = gp.snap_geometries(distance_centroids21, union_trenruta, 0.01)
connectors21 = gp.fix_geometry(connectors21)
union_trenruta21 = gp.fix_geometry(union_trenruta)
connectors21 = gp.multipart_to_singleparts(connectors21)
union_trenruta21 = gp.multipart_to_singleparts(union_trenruta21)
trenruta_split_connectors21 = gp.split_with_lines(union_trenruta21, connectors21)
connectors_split_trenruta21 = gp.split_with_lines(connectors21, union_trenruta21)
trenruta_split_connectors21 = gp.fix_geometry(trenruta_split_connectors21)
connectors_split_trenruta21 = gp.fix_geometry(connectors_split_trenruta21)
trenruta_split_connectors21 = gp.multipart_to_singleparts(trenruta_split_connectors21)
connectors_split_trenruta21 = gp.multipart_to_singleparts(connectors_split_trenruta21)
union21 = gp.union(connectors21, union_trenruta21)

######################################################################
# re-projecting and calculating length of all pieces
######################################################################
print('reprojecting and calculating lengths')
union21 = gp.reproject_layer(union21, 'ESRI:102003')
#union90 = gp.reproject_layer(union90, 'ESRI:102003')
union21 = gp.fix_geometry(union21)
#union90 = gp.fix_geometry(union90)
union21 = gp.add_length_attribute(union21, 'len_km', field_precision=6)
#union90 = gp.add_length_attribute(union90, 'len_km', field_precision=6)

formula = '''CASE
 WHEN ("cat" IS NOT NULL) AND ("ruta" IS NULL) AND ("tren" IS NULL) THEN 'ttren'
 WHEN ("tren" = 1) AND ("ruta" IS NULL) THEN 'tren'
 WHEN ("ruta" = 1) THEN 'ruta'
END
'''
union21 = gp.generic_field_calculator(union21, 'type', 'str', formula)
#union90 = gp.generic_field_calculator(union90, 'type', 'str', formula)

######################################################################
# calculating costs and final cleanup
######################################################################
print('calculating costs and final cleanup')
miles_per_km=0.6213712
dollars_per_mile_tren=0.0063
dollars_per_mile_ruta=0.0049
dollars_per_mile_ttren=0.231
formula = '''CASE
 WHEN ("type" = 'ttren') THEN "len_km"*{}
 WHEN ("type" = 'ruta') THEN "len_km"*{}
 WHEN ("type" = 'tren') THEN "len_km"*{}
END
'''.format(miles_per_km*dollars_per_mile_ttren,
		   miles_per_km*dollars_per_mile_ruta,
		   miles_per_km*dollars_per_mile_tren)
union21 = gp.generic_field_calculator(union21, 'cost', 'float', formula, field_precision=6)
#union90 = gp.generic_field_calculator(union90, 'cost', 'float', formula, field_precision=6)

################################################################
# QNEAT3 needs "speed", it does not handle "cost"
################################################################
# to calculate speed that, observe that
# cost_of_distance = length*cost_per_length
# time = length*time_per_length
# time = length/speed
# => speed = 1/time_per_length
# now equate time = cost
# length*cost_per_length = length*time_per_length
# cost_per_length = time_per_length
# cost_per_length = 1/speed
# speed = 1/cost_per_length
# note that we can do this since the gravity model does not care about units

formula = '''CASE
 WHEN ("type" = 'ttren') THEN {}
 WHEN ("type" = 'ruta') THEN {}
 WHEN ("type" = 'tren') THEN {}
END 
'''.format(1/(miles_per_km*dollars_per_mile_ttren),
		   1/(miles_per_km*dollars_per_mile_ruta),
		   1/(miles_per_km*dollars_per_mile_tren))
union21 = gp.generic_field_calculator(union21, 'speed', 'float', formula, field_precision=6)
#union90 = gp.generic_field_calculator(union90, 'speed', 'float', formula, field_precision=6)

gp.drop_fields(union21, keep_fields=['len_km', 'type', 'cost', 'speed'], output_object=out21)
#gp.drop_fields(union90, keep_fields=['len_km', 'type', 'cost', 'speed'], output_object=out90)

######################################################################
# making a copy of the centroids in the right projection 
######################################################################
print('making a copy of the centroids in the right projection ')

capitales = gp.reproject_layer(capitales, 'ESRI:102003')
centroids = gp.centroids(capitales)
gp.drop_fields(centroids, keep_fields=['NHGISNAM'], output_object=outcent)


print('DONE!')










