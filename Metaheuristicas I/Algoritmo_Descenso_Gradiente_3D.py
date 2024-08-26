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

def dev_y(x,y):
  return 3

def Gradienter_3d(alpha, x_inicial,y_inicial, precision,max_iter):
  x = x_inicial
  y = y_inicial
  i = 0
  puntos = [(x,y)]

  while i < max_iter:
    dx = dev_x(x,y)
    dy = dev_y(x,y)

    x = x - alpha * dx
    y = y - alpha * dy

    puntos.append((x,y))

    i += 1

    if abs(dx) < precision:
      break

  return x, y, i, puntos

alpha = 0.1
x_inicial = -10
y_inicial = 10
precision = 0.0001
max_iter = 1000

x_optimo, y_optimo, iteraciones,puntos = Gradienter_3d(alpha,x_inicial,y_inicial,precision,max_iter)

puntos = np.array(puntos)
x_trayectoria = puntos[:,0]
y_trayectoria = puntos[:,1]
z_trayectoria = funcion(x_trayectoria,y_trayectoria)

# Graficar la función en 3D
x_vals = np.linspace(-10, 10, 400)
y_vals = np.linspace(-10, 10, 400)
X, Y = np.meshgrid(x_vals, y_vals)
Z = funcion(X, Y)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)

# Graficar la trayectoria del descenso de gradiente
ax.plot(x_trayectoria, y_trayectoria, z_trayectoria, color='red', marker='o', label='Trayectoria', zorder=5)

# Marcar el punto final alcanzado
ax.scatter(x_optimo, y_optimo, funcion(x_optimo, y_optimo), color='red', s=100, label=f"Punto alcanzado ({x_optimo:.4f}, {y_optimo:.4f})")

# Títulos y etiquetas
ax.set_title("Descenso de Gradiente en 3D para $f(x, y) = x^2 + 3y$")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("f(x, y)")
plt.legend()
plt.show()

print(f"El valor optimo de x es:{x_optimo}")
print(f"El valor alcanzado de y es: {y_optimo}")
print(f"Número de iteraciones: {iteraciones}")
print(f"f(x,y) = x^2+3y = {funcion(x_optimo,y_optimo)}")
