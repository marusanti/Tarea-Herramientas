# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

print("Hello, World!")

x = 1
if x == 1:
  # Indented  
  print("x is 1")
  
  myint = 7
print(myint)

myfloat = 7.0
print(myfloat)
# Convertir a float
myfloat = float(myint)
# `float` es un término protegido
print(myfloat)

# Convertir float a integer
myint = int(7.8)
print(myint)

print(10 / 20)
print(10 / 2)
y= 10 / 2
print(y==5)
print(10 // 20)
print(10 // 2)
print(5.0 // 2)

# Conversión implícita
print(5 + 2.0)
# Conversión explícita
print(float(5 + 2))

mystring = "Hello, World!"
print(mystring)
mystring = "Let's talk about apostrophes..."
print(mystring)
mystring = 'Let'
print(mystring)

one = 1
two = 2
three = one + two
print(three)

hello = "Hello,"
world = "World!"
helloworld = hello + " " + world
print(helloworld)

a, b = 3, 4
print(a)
print(a, b)

a=3
b=4
n=3*4
print('El producto de', a , 'por' , b , 'es', n)
# f-string
print(f'El producto de {a} por {b} es {n}')

variable = 1/3 * 100
print("Unformated variable: {}%".format(variable))
print("Formatted variable: {:.3f}%".format(variable))
print("Space formatted variable: {:10.1f}%".format(variable))

mylist = []
mylist.append(1)
mylist.append(2)
mylist.append(3)
mylist.append(4)
# Se puede `llamar' a cada item de la lista directamente. 
# Ojo! Python empieza a contar desde 0.
print(mylist[0])
# El último item de la lista se `llama' usando el -1. 
print(mylist[-1])
# También podés seleccionar un subgrupo de items (slice)
print(mylist[1:3])

# Fundamental para hacer loops usando `for` .
# `x` es una nueva variable que toma el valor de cada item de la lista en orden.
for x in mylist:
    print(x)
    
# Agregar elementos a lista
a = [1,2,3]

#a += [4,5] 
#a += 4,5
a[len(a):] = [4,5]
#a.extend([4,5])

##Ojo!
#a.append([4,5])
#a[2:]=[4,5]

print(a)

# Imaginemos que tenemos una lista de nombres no ordenados que de alguna manera se incluyeron algunos números al azar.
# Para este ejercicio, queremos imprimir la lista alfabética de nombres sin los números.
# Esta no es la mejor manera de hacer el ejercicio, pero ilustrará un montón de técnicas.
names = ["John", 3234, 2342, 3323, "Eric", 234, "Jessica", 734978234, "Lois", 2384]
print("Number of names in list: {}".format(len(names)))    

# Primero eliminamos esos números
new_names = []
for n in names:
    if isinstance(n, str):
        # Si n es string, agregar a la lista
        # Notar la doble sangría
        new_names.append(n)

# Ahora tendríamos que tener sólo nombres en la lista. 
# Ordenémoslos
new_names.sort()
print("Cleaned-up number of names in list: {}".format(len(new_names)))        
print(new_names)

for ele in enumerate(new_names): 
    print (ele)
    
    # Veámoslos, pero enumerándolos.
for i, n in enumerate(new_names):
    # Usar i y n como string
    # Agregar 1 a i porque las listas empiezan en 0.
    print("{}. {}".format(i+1, n))

x = [10, [3.141, 20, [30, 'baz', 2.718]], 'foo']
# Para "llamar" la f de 'foo''
print(x[2][0])
print(x[2][-3])
# Para "llamar" a [3.141, 20]
print(x[1][0:2])
# Para eliminar un elemento
x[0:1]=[]
#x.remove(0)
print(x)

del x[1]
print(x)

# Extraer todos los componentes únicos de la frase
print(set("the rain is wet and wet is the rain".split()))

set_one = set(["Alice", "Carol", "Dan", "Eve", "Heidi"])
set_two = set(["Bob", "Dan", "Eve", "Grace", "Heidi"])

# Intersection (también se puede usar &)
print("Set One intersection: {}".format(set_one.intersection(set_two)))
print("Set Two intersection: {}".format(set_two.intersection(set_one)))
print("Set Two intersection:", set_two & set_one)

# Symmetric difference (también se puede usar ^)
print("Set One symmetric difference: {}".format(set_one.symmetric_difference(set_two)))
print("Set Two symmetric difference: {}".format(set_two.symmetric_difference(set_one)))
print("Set Two symmetric difference:", set_two ^ set_one)

# Difference (también se puede usar -)
print("Set One difference: {}".format(set_one.difference(set_two)))
print("Set Two difference: {}".format(set_two.difference(set_one)))
print("Set Two difference:", set_two - set_one)

# Union (también se puede usar |)
print("Set One union: {}".format(set_one.union(set_two)))
print("Set Two union: {}".format(set_two.union(set_one)))
print("Set Two union:", set_two | set_one)

# Está Bob en el set?
'Bob' in set_one

phonebook = {}
phonebook["John"] = {"Phone": "012 794 794",
                     "Email": "john@email.com"}
phonebook["Jill"] = {"Phone": "012 345 345",
                     "Email": "jill@email.com"}
phonebook["Joss"] = {"Phone": "012 321 321",
                     "Email": "joss@email.com"}
print(phonebook)

for name, record in phonebook.items():
    print("{}'s phone number is {}, and their email is {}".format(name, record["Phone"], record["Email"]))

# `del`
del phonebook["John"]
for name, record in phonebook.items():
    print("{}'s phone number is {}, and their email is {}".format(name, record["Phone"], record["Email"]))

# `pop` te muestra el registro y después lo borra
jill_record = phonebook.pop("Jill")
print(jill_record)

# Quiero el teléfono de Joss
phonebook["Joss"]["Phone"]

# False and True 
jill_record = phonebook.get("Jill", False)
if jill_record: 
    print("Jill's phone number is {}, and their email is {}".format(jill_record["Phone"], jill_record["Email"]))
else: # si es False
    print("No record found.")

number = 1 + 2 * 3 // 4
print(number)

remainder = 11 % 3
print(remainder)

squared = 7 ** 2
print(squared)

cubed = 2 ** 3
print(cubed)

even_numbers = [2, 4, 6, 8]
uneven_numbers = [1, 3, 5, 7]
all_numbers = uneven_numbers + even_numbers

# Concatenar
print(all_numbers)

# Para ordenar 
all_numbers.sort()
print(all_numbers)

# También se puede armar una secuencia repetida
print([1, 2 , 3] * 3)

# Concatenación de strings
helloworld = "Hello, " + "World!"
print(helloworld)

# Repetir secuencia
manyhellos = "Hello " * 10
print(manyhellos)

# No se puede hacer cualquier cosa...
# nohellos = "Hello " / 10
# print(nohellos)

a_string = "Hello, World!"
# Cuenta los espacios también
print("String length: {}".format(len(a_string)))

# Recordá que Python cuenta desde 0.

# Observá que hay ' dentro de "".

print("Index for first 'o': {}".format(a_string.index("o")))
print("Count of 'o': {}".format(a_string.count("o")))
print("Count of 'o' between character 4 and 8: {}".format(a_string.count("o",4,8)))
print("Count of 'o' from character 3 on: {}".format(a_string.count("o",4)))
print("Slicing between second and fifth characters: {}".format(a_string[2:6]))
print("Skipping between 3rd and 2nd-from-last characters: {}".format(a_string[3:-2:2]))
print("Reverse text: {}".format(a_string[::-1]))
print("Starts with 'Hello': {}".format(a_string.startswith("Hello")))
print("Ends with 'Hello': {}".format(a_string.endswith("Hello")))
print("Contains 'Goodbye': {}".format("Goodbye" in a_string))
print("Split the string: {}".format(a_string.split(" ")))
print("Does not split the string: {}".format(', '.join(a_string.split(", ")))) # son complementarios
print("Does not split the string: {}".format(a_string.strip(", "))) # solo si ", " está al principio o al final
print("Does not split the string: {}".format(a_string.strip("H"))) # solo si ", " está al principio o al final
print("{}".format(a_string.upper().lower())) # son complementarios

# Simple boolean tests
x = 2
print(x == 2)
print(x == 3)
print(x < 3)

# Using `and`
name = "John"
print(name == "John" and x == 2)

# Using `or`
print(name == "John" or name == "Jill")

# Using `in` on lists
print(name in ["John", "Jill", "Jess"])

x = 2
y = 10
if x > 2:
    print("x > 2")
elif x < 10 or y > 50:
    print("x < 10 or y > 50")
elif x == 2 and y > 0:
    print("x == 2 and y > 50")
else:
    print("Nothing worked.")

# Se puede escribir separando con ;
x = 2
y = 10
if x < 10 or y > 50: print("x < 10 or y > 50")

# Using `not`
name_list1 = ["John", "Jill"]
name_list2 = ["John", "Jill"]
print(not(name_list1 == name_list2))

# Using `is`
print(name_list1 == name_list2)

print(name_list1 is name_list2)

print(name_list1 is name_list1)

my_list=[1,2]

if len(my_list) != 0:
   print("Not empty!")

# Más conciso
if my_list:
   print("Not empty!")
   
# Otro ejemplo
a = 5
if a:
	print(a)
 
a = 0
if a:
	print(a)

# For
for i, x in enumerate(range(2, 8, 2)):
    print("{}. Range {}".format(i+1, x))

# While 
count = 0
while count < 5:
    print(count)
    count += 1 # Recordar que ya vimos esto
else:
    print("End of while loop reached")

# Ojo con las sangrías

# Break and while conditional
print("Break and while conditional")
count = 0
while True:
    # Esto correría para siempre a menos que pongamos el break
    print(count)
    count += 1
    if count >= 5:
        break

# Continue
print("Continue")
for x in range(8):
    # Check si x es par
    if (x+1) % 2 == 0:
        continue
    print(x)

# Pass
print("Pass")
for x in range(8):
    # Check si x es par
    if (x+1) % 2 == 0:
        pass
    print(x)
    
sentence = "for the song and the sword are birthrights sold to an usurer, but I am the last lone highwayman and I am the last adventurer"
words = sentence.split()
print(words)
word_lengths = []
for word in words:
      if word != "the":
          word_lengths.append(len(word))
print(word_lengths)

# Usando una list comprehension
sentence = "for the song and the sword are birthrights sold to an usurer, but I am the last lone highwayman and I am the last adventurer"
word_lengths = [len(word) for word in sentence.split(" ") if word != "the"]
print(word_lengths)

# Función simple sin argumentos (def function_name(parámetros):)
def say_hello():
    print("Hello, World!")

# Llamar función
say_hello()

# Testearla
print(callable(say_hello))

# Una función con dos argumentos string
def say_hello_to_user(username, greeting):
    # Devuelve saludo a un nombre
    print("Hello, {}! I hope you have a great {}.".format(username, greeting))

# Hay que "llamarla" (to call it)
say_hello_to_user("Jill", "day")

# Realizar un cálculo
def sum_two_numbers(x, y):
    # Devolver resultado
    return x + y

sum_two_numbers(5, 10)

# Realizar un cálculo
def sum_two_numbers2(x, y):
    # Devolver resultado
    print(x + y)

sum_two_numbers2(5, 10)

def add_three(num):
    return num + 3
x1 = sum_two_numbers(5, 10)
x2 = sum_two_numbers(5, 10)

print (x1)
print (x2)

x3 = add_three(x1)
print (x3)
x4 = add_three(x2)
print (x4)

def number_powered(number, exponent):
    # Devuelve el numero alevado al exponente
    return number ** exponent

# `sum_two_numbers` sigue disponible
def sum_and_power(number1, number2, exponent):
    # Devuelve los dos números sumados, y luego exponenciados
    summed = sum_two_numbers(number1, number2)
    return number_powered(summed, exponent)

# `sum_and_power`
print(sum_and_power(2, 3, 4))

def docstring_example():
    """
    An example function which returns `True`.
    """
    return True

# Imprimir el comentario
print(docstring_example.__doc__)

class myClass:
    """
    A demonstration class.
    """
    my_variable = "Look, a variable!"
    
    def my_function(self):
        """
        A demonstration class function.
        """
        return "I'm a class function!"
    
# You call a class by creating a new class object
new_class = myClass()

# You can access class variables or functions with a dotted call, as follows
print(new_class.my_variable)
print(new_class.my_function())

# Access the class docstrings
print(myClass.__doc__)
print(myClass.my_function.__doc__)

# Agregar nueva variable
new_class1 = myClass()
new_class1.my_variable2 = "Hi, Bob!"
print(new_class1.my_variable2, new_class1.my_variable)

def test_args_kwargs(arg1, arg2, arg3):
    print("arg1:", arg1)
    print("arg2:", arg2)
    print("arg3:", arg3)

#Now you can use *args or **kwargs to pass arguments to this little function. Here’s how to do it:

# first with *args
args = ("two", 3, 5)
test_args_kwargs(*args)

# now with **kwargs:
kwargs = {"arg3": 3, "arg2": "two", "arg1": 5}
test_args_kwargs(**kwargs)

class demoClass:
    """
    A demonstration class with an __init__ function, and a function that takes args and kwargs.
    """
    
    def __init__(self, argument = None):
        """
        A function that is called automatically when the demoClass is initialised.
        """
        self.demo_variable = "Hello, World!"
        self.initial_variable = argument
        
    def demo_class(self, *args, **kwargs):
        """
        A demo class that loops through any args and kwargs provided and prints them.
        """
        for i, a in enumerate(args):
            print("Arg {}: {}".format(i+1, a))
        for k, v in kwargs.items():
            print("{} - {}".format(k, v))
        if kwargs.get(self.initial_variable):
            print(self.demo_variable)
        return True

demo1 = demoClass()
demo2 = demoClass("Bob")

# What was initialised in each demo object?
print(demo1.demo_variable, demo1.initial_variable)
print(demo2.demo_variable, demo2.initial_variable)

# A demo of passing arguments and keyword arguments
args = ["Alice", "Bob", "Carol", "Dave"]
kwargs = {"Alice": "Engineer",
          "Bob": "Consultant",
          "Carol": "Lawyer",
          "Dave": "Doctor"
         }

demo2.demo_class(*args, **kwargs)

# Computed properties

class Matrix:

    def __init__(self, data):
        self._entries = list(list(float(x) for x in r) for r in data)
        for row in self._entries[1:]:
            if len(row) != self.n_cols:
                raise ValueError("rows must have the same number of entries")
        if self.n_rows == 0:
            raise ValueError("a matrix must have at least one entry")

    def __repr__(self):
        args = ", ".join("(" + ", ".join(f"{c:.3f}" for c in r) + ",)" for r in self._entries)
        return f"Matrix(({args}))"

    @property
    def n_rows(self):
        return len(self._entries)

    @property
    def n_cols(self):
        return len(self._entries[0])

m = Matrix([(1, 2, 3), (4, 5, 6)])
m.n_rows, m.n_cols
print(m)

#  Leer el manual de ayuda usando `help (module)` (va a mostrar los docstrings)
import pandas as pd

help(pd)

# Después de importar un módulo, `dir (module)` te permite ver una lista de todas las funciones implementadas en esa biblioteca.
dir(pd)

import numpy as np
import random

def generate_float_list(lwr, upr, num):
    """
    Return a list of num random decimal floats ranged between lwr and upr.
    
    Range(lwr, upr) creates a list of every integer between lwr and upr.
    random.sample takes num integers from the range list, chosen randomly.
    """
    int_list = random.sample(range(lwr, upr), num)
    return [x/100 for x in int_list]

# Create two lists
height = generate_float_list(100, 220, 10)
weight = generate_float_list(5000, 20000, 10)

# Convert these to Numpy arrays
np_height = np.array(height)
np_weight = np.array(weight)

print(np_height)
print(np_weight)

# Calculate body-mass index based on the heights and weights in our arrays
# Time the calculation ... it won't be long
bmi = np_weight / np_height ** 2

print(bmi)

# Any BMI > 35 is considered severely obese. Let's see who in our sample is at risk.

# Get a boolean response
print(bmi > 35)

# Or print only BMI values above 35
print(bmi[bmi > 35])

import pandas as pd
import numpy as np

s = pd.Series([1,3,5,np.nan,6,8])
print(s)

# Crea un DataFrame pasando una matriz numpy, con un índice de fecha y hora y columnas etiquetadas - c/ ISO-formatted date (YYYYMMDD)
dates = pd.date_range('20130101', periods=6)
print(dates)

# Create a dataframe using the date range we created above as the index
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
print(df)

# También podemos mezclar datos de texto y numéricos con un índice generado automáticamente.
dict = {"country": ["Brazil", "Russia", "India", "China", "South Africa"],
       "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria"],
       "area": [8.516, 17.10, 3.286, 9.597, 1.221],
       "population": [200.4, 143.5, 1252, 1357, 52.98] }

brics = pd.DataFrame(dict)

# Set the ISO two-letter country codes as the index
brics.index = ["BR", "RU", "IN", "CH", "SA"]

print(brics)

import matplotlib.pyplot as plt
# Para que Matplotlib plots lo muestre en notebook.


# Produce a random timeseries
ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))

# Get the cumulative sum of the random numbers generated to mimic a historic data series
ts = ts.cumsum()

# And plot
ts.plot()

# Save
plt.savefig('timeseries.png')

# And do the same thing with a dataframe
df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index,
                  columns=['A', 'B', 'C', 'D'])

df = df.cumsum()

# And plot, this time creating a figure and adding a plot and legend to it
df.plot()
plt.legend(loc='best')

# Save
plt.savefig('series.png')

