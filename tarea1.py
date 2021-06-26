#1.	Mostrar las primeras y últimas filas de la base

import pandas as pd

df = pd.read_excel (r'C:/Users/matia/Documents/UDESA/7_Herramientas/Python/Tarea-1-Python/base_tarea.xls')

print (df)

#print(df.head())

#2. Obtener los tipos de datos de las variables

print(df.dtypes)

#3.	Mostrar las primeras y últimas filas de la base de 3 columnas que elija 

print(df[["Year", "State", "Name"]])

#4.	Mostrar las estadísticas básicas (media, sd, min, max) de Production.

print(df["Production"].describe().round(decimals=1))

#5.	Insertar una columna en la quinta posición y llenala de valores NaN

import numpy as np

df.insert(5, "columna", np.nan)

#6.	Importar a un dataframe los datos saltando las primeras 10 filas. 

#df2 = pd.read_excel  (r'C:/Users/matia/Documents/UDESA/7_Herramientas/Python/Tarea-1-Python/base_tarea.xls',
#                 skiprows=10)

df2 = df.tail(1440)
print(df2)

#7.	Añadir una fila con la producción total y las horas de trabajo totales.  

df.loc['Column_Total']= df.sum(numeric_only=True, axis=0)

print(df)

#8.	Importar a un data frame las primeras 10 

df3 = df.head(10)
print(df3)

#9.	Crear un subtotal de "Horas de trabajo" por ID 

print(df.groupby(['ID'])["Labor_Hours"].sum())

#10.	Mostrar los valores para un ID de MSHA específico

print([df[df["ID"].isin([102901])]])

#11.	Mostrar aquellas observaciones en las que "Horas de trabajo" > 25000.  

print([df[df["Labor_Hours"]>25000]])

#12.	Encuentre todos los registros que incluyan dos identificaciones específicas de MSHA 

filter1 = df["State"].isin(["Alabama"])
filter2 = df["County"].isin(["Bibb", "Jackson"])
  
# displaying data with both filter applied and mandatory 
print(df[filter1 & filter2])

#13.	Ordenar los registros por la columna “Horas de trabajo” 

print(df.sort_values("Labor_Hours", ascending=False))

#14.	Haga una lista en donde date esté entre febrero 2005 y noviembre 2006 

print(df[(df['date'] > '2005-02-01') & (df['date'] < '2006-11-01')])

#15.	Mostrar la lista de aquellos cuyos date sea 2005 

print(df[(df['date'] > '2005-01-01') & (df['date'] < '2005-12-01')])

#16.	Ordenar en base a ID y date columnas dadas 

print((df.sort_values(by=['ID','date'], ascending=[0,1])))  

#17.	Crear tres hojas de datos (sheet) desde el archivo de Excel y combinarlas en un único Excel.
# Las tres hojas de datos son las mismas, sería triplicar el Excel 

df4 = pd.DataFrame([['a', 1], ['b', 2]],
                   columns=['letter', 'number'])
df5 = pd.DataFrame([['c', 3], ['d', 4]],
                   columns=['letter', 'number'])
df6 = pd.DataFrame([['e', 5], ['f', 6]],
                   columns=['letter', 'number'])

writer = pd.ExcelWriter('C:/Users/matia/Documents/UDESA/7_Herramientas/Python/Tarea-1-Python/base.xlsx', engine='xlsxwriter')
workbook = writer.book

df4.to_excel (writer,
                     sheet_name='4',
             startrow=0,
             startcol=0)
df5.to_excel (writer,
                     sheet_name='5',
             startrow=0,
             startcol=0)
df6.to_excel (writer,
                     sheet_name='6',
             startrow=0,
             startcol=0)

writer.save()

df4 = pd.read_excel (r'C:/Users/matia/Documents/UDESA/7_Herramientas/Python/Tarea-1-Python/base.xlsx',
                     sheet_name='4')
df5 = pd.read_excel (r'C:/Users/matia/Documents/UDESA/7_Herramientas/Python/Tarea-1-Python/base.xlsx',
                     sheet_name='5')
df6 = pd.read_excel (r'C:/Users/matia/Documents/UDESA/7_Herramientas/Python/Tarea-1-Python/base.xlsx',
                     sheet_name='6')
        
print(pd.concat([df4, df5, df6]))

#18.	Dibujar un gráfico de barras comparando el año, el ID, la producción y las horas de trabajo de las primeras 10 observaciones 

df['Año'] = df['date'].dt.year #armo columna año para usarla
df3= df.head(n=10)
import matplotlib.pyplot as plt
plotear = df3[['Año', 'ID', 'Production','Labor_Hours']]
ax = plt.gca() 
plotear.plot(kind='bar',x='ID',y='Production',color='red',ax=ax)
plotear.plot(kind='bar',x='ID',y='Labor_Hours',color='orange',ax=ax)
plt.show()

#19.	Dibujar un gráfico de barras de las 10 empresas con mayor producción 
#Grafico para el top 10 de empresas 2006
plotear2 = df[df['Año'] == 2006] #filtro año 2006
plotear2.dropna(subset=['Production']) #quito valores na de produccion
plotear2 = plotear2.sort_values("Production",ascending=False) #ordeno
plotear2 = plotear2.head(n=10)
plotear2 = plotear2[['Name', 'Production']]#me quedo con variables que voy a usar

plotear2.plot(kind='bar',x='Name',y='Production',color='green') #grafico
plt.show()

