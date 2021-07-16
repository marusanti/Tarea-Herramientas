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


tmap <- tm_shape(lnd) +
  tm_polygons("CrimeCount_pc",
              palette = "Reds",
              border.col = "white",
              breaks = c(0, 50, 75, 100, 200, 300, 400),
              midpoint = 0.7,
              title = c("")) + 
  tm_scale_bar(position = c("center", "top"),
               text.color="white", width = 0.2, text.size = 0.8) +
  tm_layout(
    bg.color="steelblue",#cambie el blue
    inner.margins = 0.15,
    frame = FALSE,
    main.title = "Theft & Handling in London",
    title = "Cases (per 1000 people)",
    main.title.position = c("left", "top"),
    title.position = c("left", "top"),
    legend.position = c("left","top"),
    main.title.color = "white",
    title.color = "white",
    legend.text.color = "white",
    main.title.fontface = 2,
    main.title.size = 1.5,
    title.size = 1.2,
    legend.text.size = 0.85,
    legend.bg.color = "steelblue",#cambie el blue
    legend.bg.alpha = 0)

tmap

#Exportar
tmap_save(tm=tmap, "output/London_R_tmap_v2.png", dpi = 300, width = 18, height = 16, units = "cm")

#Plotear con GG
lnd_f <- broom::tidy(lnd)
lnd$id <- row.names(lnd) 
head(lnd@data, n = 2) 
lnd_f <- left_join(lnd_f, lnd@data)

mapgg2 <- ggplot(lnd_f, aes(long, lat, group = group,
                            fill = CrimeCount_pc)) +
  geom_polygon(colour = "red", size = 0.4) + coord_equal() +
  annotate(geom="text", x=525118.5, y=181295.6,
           label="Westminster", color="black", size=9) +#cambie aca
  annotate(geom="text", x=549169.8, y=175905.6,
           label="Bexley", color="black", size=9) +#cambie aca
  scale_fill_gradient2(low="hotpink1",midpoint = -200, high="hotpink4", na.value= "white") +
  ggtitle("Hurtos en Londres en 2001", 
          subtitle ="Casos registrados por distrito cada 1000 habitantes.") +
  theme(plot.title=element_text(color="cadetblue4",size=40, hjust = -0.2, face="bold"),
        plot.subtitle=element_text(color="cadetblue4",size=30, hjust = -0.41, face="bold"),
        panel.background = element_rect(fill = "white", colour = "white"),
        panel.grid=element_blank(),
        legend.position = c(-.1, .95),
        legend.justification = c("left", "top"),
        legend.key.size = unit(2, 'cm'),
        legend.box.just = "left",
        legend.text=element_text(size=22),
        legend.title = element_blank(),
        legend.key = element_rect(color=3,fill="gray97"),
        axis.title=element_blank(),
        axis.text=element_blank(),
        axis.ticks=element_blank())

mapgg2

#Exportar
ggsave("output/London_R_gg2_v2.png", dpi = 300, width = 50, height = 30, units = "cm")


