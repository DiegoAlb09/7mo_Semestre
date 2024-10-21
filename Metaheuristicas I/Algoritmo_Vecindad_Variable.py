# Variable Neighborhood Search (VNS) Algorithm
import numpy as np
import random
import matplotlib.pyplot as plt

# Función de costo que se desea minimizar 
def function_cost(x):
  return x**2

# Generarción de una solción aleatoria inicial
def initial_solution(size):
  return [random.randint(-10, 10) for _ in range(size)]

# Generación de un vecindario
def neighborhood(x, size):
  new_solution = x[:]
  for _ in range(size):
    #Cambiar un valor aleatorio de la solución
    index = random.randint(0, len(x)-1)
    new_solution[index] = random.randint(-10, 10)
  return new_solution

