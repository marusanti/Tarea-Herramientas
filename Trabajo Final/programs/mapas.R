########################
# Importamos librerias
######################
x <- c("ggmap", "rgdal", "rgeos", "maptools", "dplyr", "tidyr", "tmap")
lapply(x, library, character.only = TRUE)

#install.packages("wesanderson")

library(wesanderson)
library(gdata)
library(ggplot2)
library(readr)
library(grid)
library(tibble)
library(gridExtra)
library(dplyr)
library(Lock5Data)
library(ggthemes)
library(fun)
library(maps)
library(mapproj)
library(tidyverse)
library(haven)

#########################
# Grafico heights France
########################
rm(list=ls())
alt <- read_dta("programs/France_heights_for_web.dta")

#Nos quedamos con soldados mayores de 21
alt <- subset(alt, AGE>20)
count(alt, PROVINC)

#hacemos dos cat, para juntar mas datos
alt$BIRTHDEC <- ifelse((alt$BIRTHDEC<1681), "1660-1680", ifelse((alt$BIRTHDEC>1739),"1740-1760", "NA"))

#agrupamos por provincia y decadas
ag <- aggregate(.~BIRTHDEC+PROVINC, alt, FUN = function(x) mean(as.numeric(as.character(x))))
ag$PROVINC <- as.character(ag$PROVINC) 
is.numeric(ag$PROVINC)
is.numeric(ag$BIRTHDEC)

#nos quedamos con pares prov-decada de mas de 30 obs
sum <- count(alt, PROVINC, BIRTHDEC)
sum <- subset(sum, n>29)

ag <- left_join(sum, ag, by=c("PROVINC", "BIRTHDEC"))
ag <- subset(ag, BIRTHDEC!="NA")
dumbell <- subset(ag, PROVINC=="CHAMPAGNE" | PROVINC=="FLANDRE" | PROVINC== "ILE DE FRANCE" | PROVINC== "LORRAINE" | PROVINC== "LYONNAIS" | PROVINC== "NORMANDIE" | PROVINC== "PICARDIE")

dumbell <- dumbell %>%
  mutate(paired = rep(1:(n()/2),each=2),
         BIRTHDEC=factor(BIRTHDEC))
dumbell$Nacimiento <- dumbell$BIRTHDEC

dumbell %>%
  ggplot(aes(x= HEIGHT, y= reorder(PROVINC,HEIGHT))) +
  geom_line(aes(group =paired),color="grey")+
  geom_point(aes(color=Nacimiento), size=6) +
  labs(y="", x="Pulgadas francesas")+
  theme_classic(15)+
  theme(legend.position="top") +
  ggtitle("Altura de soldados mayores de 21 en provincias francesas") +
  scale_color_brewer(palette="Accent", direction=-1) +
  ggsave("output/france.jpg")

################################
#cargamos datos para animacion poblacion
################################
rm(list=ls())

countries <- readOGR(dsn = "data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp")
countries <- rename.vars(countries, c("SU_A3"), c("isocode"))
countries <- subset(countries, select=c("isocode"))

pop <- read_dta("programs/country_level_panel_for_web.dta")
pop <- subset(pop, select=c("isocode", "population", "total_land_area", "year", "cont_africa", "cont_asia", "cont_europe"))

#creamos variable de densidad pobalcional
#pop$density <- log(pop$population)/log(pop$total_land_area)
pop$density <- pop$population/pop$total_land_area
hist(pop$density) #pasamos alog scale con la funcion gradient_scale despues

# coordinate reference system (CRS) 
countries@proj4string

##########
#Join
#########
## ggmap  data.frame, using tidy()
countries_f <- broom::tidy(countries)
names(countries_f)

# This step has lost the attribute information associated with the countries object
countries$id <- row.names(countries@data) 
head(countries@data, n = 5)
countries_f <- left_join(countries_f, countries@data) 
countries_f <- left_join(countries_f, pop)

#########
# Subsets
#########
rm(pop, countries)
countries_f <- subset(countries_f, select=c("group", "isocode", "lat", "long", "density", "year", "cont_africa", "cont_asia", "cont_europe"))
countries_f <- subset(countries_f, density>0)
countries_f <- subset(countries_f, year==1500 | year==1900)
europe_f <- subset(countries_f, cont_europe==1)# & isocode!="RUS") 
#africa_f <- subset(countries_f, cont_africa==1)
europe_f_1500 <- subset(europe_f, europe_f$year>"1450")# | isocode!="RUS")
europe_f_1500 <- subset(europe_f_1500, isocode=="")
europe_f_1500 <- europe_f_1500[,-(7:9)]   
europe_f_1500 <- europe_f_1500[,-(2)]   

#######
#Plot
######

pal <- wes_palette("Zissou1", 100, type = "continuous") #paleta de colores linda

memory.limit(4000)

#world
ggplot(data = countries_f, # the input data
       aes(x = long, y = lat, fill = density, group = group)) + # define variables
  geom_polygon() + 
  geom_path(colour="black", lwd=0.025) + 
  coord_equal(xlim=c(-15,180), ylim=c(-46,82)) + # fixed x and y scales
  facet_wrap(~ year) + 
  scale_fill_gradientn(colours=pal, na.value = NA, breaks=c(1, 10, 1000), trans = "log", guide = guide_colourbar(direction = "horizontal"), position =c("left"), labels = function(x) sprintf("%.0f", x), name="Densidad (personas/km2)") + # legend options, con un decimal
  ggtitle("Evolución de la población en el mundo") +
  theme(legend.position="top",
        legend.key.size = unit(0.9, 'cm'),
        axis.text = element_blank(), 
        axis.title = element_blank(), # remove axis titles
        axis.ticks = element_blank(),
        panel.background = element_rect(fill ="white", colour = "white"),  #fondo blanco
        plot.background=element_rect(fill="white"),
        panel.grid.major = element_line(color="white",linetype=1)) +
  ggsave("output/map_pop_world.jpg")

#europe
ggplot(data = europe_f, # the input data
       aes(x = long, y = lat, fill = density, group = group)) + # define variables
  geom_polygon() + 
  geom_path(colour="black", lwd=0.025) + 
  coord_equal(xlim=c(-10,40), ylim=c(35,70)) + # fixed x and y scales
  facet_wrap(~ year) + 
  scale_fill_gradientn(colours=pal, na.value = NA, breaks=c(1, 10, 100, 1000), trans = "log", guide = guide_colourbar(direction = "horizontal"), position = c("left"), labels = function(x) sprintf("%.0f", x), name="Densidad (personas/km2)") + # legend options, con un decimal
  ggtitle("Evolución de la población en Europa") +
  theme(legend.position="top",
        legend.key.size = unit(0.9, 'cm'),
        axis.text = element_blank(), 
        axis.title = element_blank(), # remove axis titles
        axis.ticks = element_blank(),
        panel.background = element_rect(fill ="white", colour = "white"),  #fondo blanco
        plot.background=element_rect(fill="white"),
        panel.grid.major = element_line(color="white",linetype=1)) +
  ggsave("output/map_pop_europe.jpg")


#####################
#animated map
####################
# Algunos paquetes necesarios
#install.packages("remotes")
#install.packages("gifski")
#remotes::install_github("thomasp85/gganimate",force = TRUE)
#remotes::install_github("thomasp85/transformr")
#install.packages("ndtv")

pkgs = c("ggmap", "sp", "tmap", "rgeos", "maptools", "dplyr")
lapply(pkgs, library, character.only = TRUE)
library(gifski)
library(gganimate)
library(transformr)
library(ggplot2)

# year as numeric format
europe_f_1500$year <- as.integer(europe_f_1500$year)

p <- ggplot(data = europe_f_1500, # the input data
            aes(x = long, y = lat, fill = density, group = group)) + # define variables
  geom_polygon() + 
  geom_path(colour="black", lwd=0.025) + 
  coord_equal(xlim=c(-10,40), ylim=c(35,70)) + # fixed x and y scales
  scale_fill_gradientn(colours=pal, na.value = NA, trans = "log", breaks=c(1, 10, 100, 1000), guide = guide_colourbar(direction = "horizontal"), position = c("left"), labels = function(x) sprintf("%.0f", x), name="Densidad (personas/km2)") + # legend options, con un decimal
  theme(legend.position="top",
        axis.text = element_blank(), 
        axis.title = element_blank(), # remove axis titles
        axis.ticks = element_blank(),
        panel.background = element_rect(fill ="white", colour = "white"),  #fondo blanco
        plot.background=element_rect(fill="white"),
        panel.grid.major = element_line(color="white",linetype=1)) +
  labs(title = 'Año: {as.integer(frame_time)}') +
  transition_time(year)

rm(europe_f, europe_f_1500, countries_f, pal, pkgs)

gc()
memory.limit(4000)
#help(animate)  
animate(p, duration = 10, width = 0.1, height = 0.1, res = 0.05, renderer = gifski_renderer())

#animate(p, renderer = ffmpeg_renderer())
anim_save("output/europe_pop.gif")
