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
library(grid)


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

#Grafico corregido v2
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
        panel.background = element_rect(fill = "white", colour = "white"), #el grid no aporta nada
        legend.title = element_blank())+ #es redundante el titulo de la legenda
  labs(title="Votos a Obama por estados",subtitle="En porcentaje")
ggsave("graficos/Obamavote2_v2.png")


####2. Base Loans ####
#grafico de clase
df3 <- read.csv("data/LoanStats.csv")
t <- subset(df3,grade=="A")
z1 <- ggplot(t, aes(total_pymnt_inv,total_rec_prncp,color=grade)) + 
  geom_point() + stat_smooth(method=lm)

z2 <- ggplot(t, aes(funded_amnt,total_pymnt_inv,color=grade)) +
  geom_point() + stat_smooth(method=lm,color=2)
s1<-grid.arrange(z1,z2,ncol=2)
ggsave("graficos/scatter plot1.png",s1,width = 6)

#Repite la leyenda, repite las escalas. Poner título y cambiar ejes
#Queda mejor a la vista con numeros en miles
#Corregido
t<-t %>% mutate(total_rec_prncp=total_rec_prncp/1000,
                total_pymnt_inv=total_pymnt_inv/1000,
                funded_amnt=funded_amnt/1000)
z1 <- ggplot(t, aes(total_rec_prncp,total_pymnt_inv,color=grade)) + 
  geom_point() +
  theme_classic()+ 
  theme(legend.position = "none")+
  ylim(0,40)+
  xlab("Principal recibido")+
  ylab("Total pagos recibidos")+
  stat_smooth(method=lm,color=2)+
  theme(axis.title.y=element_text(size=8),
        axis.title.x=element_text(size=8))

z2 <- ggplot(t, aes(funded_amnt,total_pymnt_inv,color=grade)) +
  geom_point() + 
  theme_classic()+
  theme(axis.title.y=element_blank(),
        legend.position = "none",
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        axis.title.x=element_text(size=8))+
  xlab("Monto total del préstamo")+
  ylim(0,40)+
  stat_smooth(method=lm,color=2)

s2<-grid.arrange(z1,z2,ncol=2,
                 top=textGrob("Variables relacionadas con los pagos de clientes de calificación credicitia A
                              (en miles de USD)", gp=gpar(fontsize=8)),
             widths=c(1,0.9))
ggsave("graficos/scatter plot2.png",s2)

####3.BAse Loans####
#Supongamos que un banco ha concedido préstamos a personas con características diferentes (por ejemplo, situación laboral, propiedad de la vivienda, grado de crédito, etc.) y queremos ver las relaciones entre algunas de esas variables.
#Objetivo: Ver la distribución de la cantidad de préstamo frente a ser propietario de una casa usando diferentes colores según el nivel de crédito".

dfn <- df3[,c("home_ownership","loan_amnt","grade")]
dfn <- na.omit(dfn) #remove NA y NONE
dfn <- subset(dfn, !dfn$home_ownership %in% c("NONE"))
g1<-ggplot(dfn,aes(x=home_ownership,y=loan_amnt))+geom_boxplot(aes(fill=grade))
ggsave("graficos/loans1.png",g1)
#Notas
#People with higher credit grades take smaller loans
#People with lower credit grades take small loans if they don't have a mortgage.
#Corregido
dfn<-dfn %>% 
    mutate(loan_amnt=loan_amnt/1000)
g2<-ggplot(dfn,aes(x=grade,y=loan_amnt))+
  geom_boxplot(aes(fill=grade))+
  facet_grid(~ home_ownership) +
  theme_minimal()+
  labs(title= "Loans according to credit grade and home ownership",
       subtitle="Thousand dolars")+
  theme(legend.position="none",
        axis.title.y = element_blank(),
        axis.title.x = element_blank(),
        title =element_text(size=8, face='bold'))
ggsave("graficos/loans2.png",g2)
#Otra propuesta:
dfn<-dfn %>%  
  group_by(home_ownership,grade) %>% 
  mutate(loan_mean=mean(loan_amnt)) %>% 
  select(loan_mean,grade,home_ownership) %>% unique()

g3<-ggplot(dfn,aes(x = grade, y = loan_mean,fill=grade)) +
  geom_bar(stat = "identity") +
  facet_grid(~ home_ownership) + 
  theme_minimal()+
  labs(title= "Average loan amount by credit grade and home ownership",
       subtitle="Thousand dolars")+
  theme(legend.position="none",
        axis.title.y = element_blank(),
        axis.title.x = element_blank(),
        title =element_text(size=7, face='bold'))
ggsave("graficos/loans3.png",g3)



