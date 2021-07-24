library(foreign)
library(tidyverse)
base1<-read.dta("../../city_level_panel_for_web.dta")
base2<-read.dta("../../country_level_panel_for_web.dta")
base3<-read.dta("../../Europe_only_city_level_panel_for_web.dta")
base4<-read.dta("../../France_heights_for_web.dta")

write.csv(base1,"city_level_panel_for_web.csv",row.names = F)
write.csv(base2,"Country_level_panel_for_web.csv",row.names = F)
write.csv(base3,"Europe_only_city_level_panel_for_web.csv",
          row.names = F)
write.csv(base4,"France_heights_for_web.csv",row.names = F)

## Bases anuales
base2_Anio_1600<-base2 %>% 
  filter(year==1600)
base2_Anio_1700<-base2 %>% 
  filter(year==1700)
base2_Anio_1800<-base2 %>% 
  filter(year==1800)
base2_Anio_1900<-base2 %>% 
  filter(year==1900)

write.csv(base2_Anio_1600,
          "Country_level_panel_for_web_1600.csv",row.names = F)
write.csv(base2_Anio_1700,
          "Country_level_panel_for_web_1700.csv",row.names = F)
write.csv(base2_Anio_1800,
          "Country_level_panel_for_web_1800.csv",
          row.names = F)
write.csv(base2_Anio_1900,
          "Country_level_panel_for_web_1900.csv",row.names = F)


