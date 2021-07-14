#Crime in London
rm(list=ls())

#Libraries
library("ggplot2")
library("tibble")
library("gridExtra")
library("dplyr")
library("Lock5Data")
library("ggthemes")
library("fun")
library("zoo")
library("corrplot")
library("maps")
library("mapproj")

#Pathname 
setwd("~/UDESA/7_HComp/Tarea-Herramientas/4-Visualization/Tarea2")

getwd()

#Importar data
library(rgdal)
lnd <- readOGR(dsn = "data/london_sport.shp")

lnd$Pop_2001 <- as.numeric(as.character(lnd$Pop_2001))
sapply(lnd@data, class)
lnd@proj4string

crime_data <- read.csv("data/mps-recordedcrime-borough.csv",
                       stringsAsFactors = FALSE)

crime_theft <- crime_data[crime_data$CrimeType == "Theft & Handling", ]

crime_ag <- aggregate(CrimeCount ~ Borough, FUN = sum, data = crime_theft)

lnd$name[!lnd$name %in% crime_ag$Borough]

#Merge
library(dplyr)

lnd@data <- left_join(lnd@data, crime_ag, by = c('name' = 'Borough'))

#Crime per capita
lnd@data$CrimeCount_pc <- lnd@data$CrimeCount/lnd@data$Pop_2001*1000

# Plotear con tmap
library(tmap) 


tmap <- qtm(shp = lnd, style="cobalt",  fill = "CrimeCount_pc", fill.palette = "Reds", fill.title = "Cases (per 1000 people)", title="Theft & Handling in London") + tm_borders(alpha=.5) 

#Exportar
tmap_save(tm=tmap, "London_R_tmap.png", dpi = 300, width = 23, height = 17, units = "cm")

#Plotear con GG
lnd_f <- broom::tidy(lnd)
lnd$id <- row.names(lnd) 
head(lnd@data, n = 2) 
lnd_f <- left_join(lnd_f, lnd@data)

map <- ggplot(lnd_f, aes(long, lat, group = group, fill = CrimeCount_pc)) +
  geom_polygon() + coord_equal() +
  annotate(geom="text", x=525118.5, y=181295.6, label="Westminster", color="white", size=9) +
  annotate(geom="text", x=549169.8, y=175905.6, label="Bexley", color="white", size=9) +
  scale_fill_gradient(low = "blue", high = "red", na.value= "white") +
  ggtitle("Hurtos en Londres en 2001", subtitle ="Casos registrados por distrito cada 1000 habitantes.") +
  theme(plot.title=element_text(color="cadetblue4",size=40, hjust = -0.2, face="bold"),
        plot.subtitle=element_text(color="black",size=30, hjust = -0.41, face="bold"),
        panel.background = element_rect(fill = "white", colour = "white"),
        panel.grid=element_blank(),
        legend.position = c(-.1, .95),
        legend.justification = c("left", "top"),
        legend.key.size = unit(2, 'cm'),
        legend.box.just = "right",
        legend.text=element_text(size=22),
        legend.title = element_blank(),
        legend.key = element_rect(color=3,fill="gray97"),
        axis.title=element_blank(),
        axis.text=element_blank(),
        axis.ticks=element_blank())

#Exportar
ggsave("London_R_gg.png", dpi = 300, width = 50, height = 30, units = "cm")


## Opcion 2 
map2 <- ggplot(lnd_f, aes(long, lat, group = group, fill = CrimeCount_pc)) +
  geom_polygon() + coord_equal() +
  annotate(geom="text", x=525118.5, y=181295.6, label="Westminster", color="white", size=9) +
  annotate(geom="text", x=549169.8, y=175905.6, label="Bexley", color="white", size=9) +
  scale_fill_gradient(low="lightpink1",high="hotpink4", na.value= "white") +
  ggtitle("Hurtos en Londres en 2001", subtitle ="Casos registrados por distrito cada 1000 habitantes.") +
  theme(plot.title=element_text(color="cadetblue4",size=40, hjust = -0.2, face="bold"),
        plot.subtitle=element_text(color="black",size=30, hjust = -0.41, face="bold"),
        panel.background = element_rect(fill = "white", colour = "white"),
        panel.grid=element_blank(),
        legend.position = c(-.1, .95),
        legend.justification = c("left", "top"),
        legend.key.size = unit(2, 'cm'),
        legend.box.just = "right",
        legend.text=element_text(size=22),
        legend.title = element_blank(),
        legend.key = element_rect(color=3,fill="gray97"),
        axis.title=element_blank(),
        axis.text=element_blank(),
        axis.ticks=element_blank())

#Exportar
ggsave("London_R_gg2.png", dpi = 300, width = 50, height = 30, units = "cm")


