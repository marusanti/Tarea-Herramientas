********************* 
** Crime in London **
*********************

global DATA = "C:/Users/matia/Documents/UDESA/7_HComp/Tarea-Herramientas/4-Visualization/Tarea2/data" 
cd "$DATA"

*Instalar paquetes

ssc install spmap
ssc install shp2dta

net install spwmatrix, from(http://fmwww.bc.edu/RePEc/bocode/s)

*Shape en Stata

shp2dta using london_sport.shp, database(ls) coord(coord_ls) genc(c) genid(id) replace

use ls, clear
describe

use coord_ls, clear
describe

*Importamos y transformamos los datos de Excel a formato Stata */
import delimited "$DATA/mps-recordedcrime-borough.csv", clear 

rename borough name

collapse (sum) crimecount, by(name)
save "crime.dta", replace

describe

*Merge
use ls, clear
merge 1:1 name using crime.dta
drop _m

*Generar crime per capita
gen crime_pc= crimecount/Pop_2001*1000
save london_crime_shp.dta, replace

* Representación por medio de mapas

use london_crime_shp.dta, clear

* Mapa de cuantiles. Editado manualmente

spmap crime_pc using coord_ls, id(id) clmethod(q) cln(6) title("Número de crímenes") legend(size(medium) position(5) xoffset(15.05)) fcolor(Blues) plotregion(margin(b+15)) ndfcolor(gray) name(g2,replace)  

