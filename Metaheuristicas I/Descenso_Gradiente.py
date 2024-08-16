import numpy as np
import matplotlib.pyplot as plt

#Definimos la funcion

def funcion(x):
  return (2*x**2)*np.cos(x) - 5*x

def df(x):
  return (4*x*np.cos(x))-(2*x**2*np.sin(x)-5)

def descenso_gradiente(alpha, x_inicial, precision, max_iter):
  x = x_inicial
  iteracion = 0

  while abs(df(x)) > precision and iteracion < max_iter:
    x = x - alpha * df(x)
    iteracion += 1

  return x, iteracion

alpha = 0.01
x_inicial = 1
precision = 0.0001
max_iter = 1000

x_optimo, iteraciones = descenso_gradiente(alpha,x_inicial,precision,max_iter)

print(f"El valor óptimo de x es: {x_optimo}")
print(f"El número de iteraciones: {iteraciones}")

x_vals = np.linspace(-5, 5, 400)
y_vals = funcion(x_vals)

plt.figure(figsize=(8,6))
plt.plot(x_vals, y_vals, label=r"$f(X)=2x^2cos(x)-5x$", color='blue')

plt.scatter(x_optimo,funcion(x_optimo),color='red', zorder=5, label=f"Min en x={x_optimo:.4f}")

plt.title("Descenso de Gradiente aplicado a $f(x)=2x^2cos(x)-5x$")
plt.xlabel("x")
plt.ylabel("y")
plt.axhline(0,color='black',linewidth=0.5)
plt.axvline(0,color='black',linewidth=0.5)
plt.legend()
plt.grid(True)

plt.show()