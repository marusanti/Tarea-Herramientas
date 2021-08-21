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

################
#cargamos datos
###############
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
countries_f <- subset(countries_f, density>0) #remove NA
europe_f <- subset(countries_f, cont_europe==1)# & isocode!="RUS") 
#africa_f <- subset(countries_f, cont_africa==1)

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
  theme(legend.position="top",
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
  theme(legend.position="top",
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
countries_f$year <- as.integer(countries_f$year)

p <- ggplot(data = europe_f, # the input data
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

memory.limit(4000)

rm(europe_f, countries_f, pal, pkgs)

#help(animate)
animate(p, duration = 10, renderer = gifski_renderer())
#animate(p, renderer = ffmpeg_renderer())
anim_save("output/europe_pop.gif")


