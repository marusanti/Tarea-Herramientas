# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 11:00:59 2021

@author: Matias Harari
"""
#!pip install wwo-hist

#### Import package

from wwo_hist import retrieve_hist_data


#### Set working directory to store output csv file(s)

import os
os.chdir("C:/Users/matia/Documents/UDESA/7_HComp/3-Scrapping")

#### Example code

frequency=12
start_date = '01-JAN-2015'
end_date = '31-DEC-2015'
api_key = '11f0449b9cea4c0db84135407210507'
#=CONCAT(CHAR(34),A3, CHAR(34), CHAR(44))
location_list = ["21505", "21606",	"21638",	"21639",	"21643",	"21651",	"21701",	"21742",	"21804",	"21811",	"21853",	"21914"]

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)