setwd("C:/Users/matia/Documents/UDESA/7_HComp/Tarea-Herramientas/2-QGIS")
rm(list=ls())

library(stargazer) # Info en https://cran.r-project.org/web/packages/stargazer/stargazer.pdf 
library(tidyverse) # librer?a muy usada para manipular los datos y hacer gr?ficos ('subpacketes' dentro)
library(ggplot2)

chic <- read.csv("Chic_AIRBNB.csv")

names(chic)

chic <- subset(chic, rev_rating>0)

reg <- lm(data=chic, rev_rating ~ response_r + accept_r + log(price_pp) + num_spots+ log(population) + crowded + harship_in + num_theft, robust=TRUE)

stargazer(reg, type='latex',
          summary = FALSE,
          flip = FALSE,
          digits=2,
          out="chic.tex") 
           


