#Ejemplo
#Sea la funcion f(x,y)=x^2+3y
#Calcular la derivada parcial de la funcion: f(x,y)=x^2+3y, entonces el f es la siguiente f = [2x, 3]
#Paso 1. Tome un punto al azar: Xo 
#f(-10, 10) = (-10)^2 + 3(10) = 130
#sea Xo [-10, 10] entonces f(Xo)=100+30
#Paso 2. Calcular el graditente 130/f(Xo)
#si f(x,y)=x^2+3y, entonces el f es [2x, 3]
#Paso 3. Camine en dirección opuesta a la pendiente:
#x1 = [-10, 10] -0.1*[-20 3] = -8 9.7

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Definimos la funcion 
def funcion(x,y):
  return x**2 + 3*y

#Definimos las derivadas parciales
def dev_x(x,y):
  return 2*x