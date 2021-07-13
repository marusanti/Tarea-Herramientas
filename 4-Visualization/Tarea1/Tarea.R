library(ggplot2)
library(tidyverse)
library(ggthemes)
library("gridExtra")
library("fun")
library("zoo")
library("corrplot")
library("maps")
library("mapproj")
library("Lock5Data")


##Correcciones
####1. Grafico Voter Chart for 2012 Elections ####
#% de votos a Obama en cada estado
#Grafico incorrecto
states_map <- map_data("state")
USStates$Statelower <- as.character(tolower(USStates$State))
us_data <- merge(USStates,states_map,by.x="Statelower",by.y="region")
ggplot(us_data, aes(x=long, y=lat, group=group, fill=ObamaVote)) + geom_polygon(colour="black") +
  coord_map("mercator")+scale_fill_gradient(low="red",high="blue")
ggsave("graficos/Obamavote1.png")

#Grafico corregido
#Tiene elementos de más
#Colores muy chillones
#Me parece que queda mejor poner el porcentaje que la proporcion
us_data<-us_data %>%  mutate(ObamaVote=ObamaVote*100)
ggplot(us_data, aes(x=long, y=lat, group=group, fill=ObamaVote)) + 
  geom_polygon(colour="black") +
  coord_map("mercator")+scale_fill_gradient(low="lightpink1",high="hotpink4")+
  theme(axis.title.x=element_blank(),#esto es para sacar el titulo del eje
        axis.text.x=element_blank(), #esto es para sacar los numeritos/texto 
        axis.ticks.x=element_blank(),#esto es para sacar las barritas del eje
        axis.title.y=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        legend.title = element_blank())+ #es redundante el titulo de la legenda
  labs(title="Votos a Obama por estados",subtitle="En porcentaje")
ggsave("graficos/Obamavote2.png")

#Ver algunas de estas opciones
####2. ####

# Aim: To make a scatter plot for the most correlated variables and then fit a linear regression model to it.”
df3 <- read.csv("data/LoanStats.csv")
t <- subset(df3,grade=="A")
z1 <- ggplot(t, aes(total_pymnt_inv,total_rec_prncp,color=grade)) + 
  geom_point() + stat_smooth(method=lm)

z2 <- ggplot(t, aes(funded_amnt,total_pymnt_inv,color=grade)) +
  geom_point() + stat_smooth(method=lm,color=2)

grid.arrange(z1,z2,ncol=2)

#REpite la leyenda, repite las escalas. Poner título y cambiar ejes
#Queda mejor a la vista con numeros en miles
#Corregido
t<-t %>% mutate(total_rec_prncp=total_rec_prncp/10000,
                total_pymnt_inv=total_pymnt_inv/10000,
                funded_amnt=funded_amnt/10000)
z1 <- ggplot(t, aes(total_rec_prncp,total_pymnt_inv,color=grade)) + 
  geom_point() +
  theme_classic()+ 
  theme(legend.position = "none")+
  ylim(0,4)+
  xlab("variable")+
  ylab("variable")+
  stat_smooth(method=lm)

z2 <- ggplot(t, aes(funded_amnt,total_pymnt_inv,color=grade)) +
  geom_point() + 
  theme_classic()+
  theme(axis.title.y=element_blank(),
        legend.position = "none",
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank())+
  xlab("variable")+
  ylim(0,4)+
  stat_smooth(method=lm,color=2)


grid.arrange(z1,z2,ncol=2, top ="Relación entre - en miles",
             widths=c(1,0.9))

####2.Consumo de electricidad y GDP pc####
df <- read.csv("data/gapminder-data.csv")
p <- ggplot(df, aes(x=gdp_per_capita, y=Electricity_consumption_per_capita)) + 
  geom_point()
p + facet_grid(Country ~ .)
p <- ggplot(df, aes(x=gdp_per_capita, y=Electricity_consumption_per_capita,
                    colour=Country)) + 
  geom_point()
p

##
dfs <- subset(df,Country %in% c("Germany","India","China","United States","Japan"))
ggplot(dfs,aes(x=Year,y=Electricity_consumption_per_capita)) + 
  geom_point(aes(size=population,color=Country))+
  coord_cartesian(xlim=c(1950,2020))+
  labs(subtitle="Electricity consumption vs Year",
       title="Bubble chart")+ylab("Electricity consumption")+
  scale_size(breaks=c(0,1e+8,0.3e+9,0.5e+9,1e+9,1.5e+9),range=c(1,5))


ggplot(dfs,aes(x=Year,y=Electricity_consumption_per_capita)) + 
  geom_line(fun.y=population) +
  coord_cartesian(xlim=c(1950,2020))+
  facet_wrap(~Country)


##
colnames(dfs1) <- c("gdp","electricity","mort","pov","bmi_m","bmi_f")
M <- cor(dfs1)
corrplot(M,method="color", order = 'alphabet')

corrplot(M,
         order = 'AOE', addCoef.col = 'black', tl.pos = 'd',
         cl.pos = 'n', col = "red")

corrplot(M,method="circle", order = 'AOE')
#https://cran.r-project.org/web/packages/corrplot/vignettes/corrplot-intro.html



##### Fin tarea 1 #####