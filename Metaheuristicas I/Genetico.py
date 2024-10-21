#Algoritmo genetico binario que converga en 20 unos con seleccion por ruleta y mutacion por inversion
import random

# Parámetros
tamaño_población = 100
longitud_cromosoma = 20
prob_mutación = 0.01
max_generaciones = 1000

# Función de evaluación (fitness)
def fitness(cromosoma):
    return sum(cromosoma)

# Selección por ruleta
def seleccion_ruleta(población):
    suma_fitness = sum(fitness(c) for c in población)
    seleccionados = []
    for _ in range(2):
        pick = random.uniform(0, suma_fitness)
        actual = 0
        for c in población:
            actual += fitness(c)
            if actual >= pick:
                seleccionados.append(c)
                break
    return seleccionados

# Cruce de un punto
def cruce(padre1, padre2):
    punto_cruce = random.randint(1, longitud_cromosoma - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2

# Mutación
def mutar(cromosoma):
    for i in range(len(cromosoma)):
        if random.random() < prob_mutación:
            cromosoma[i] = 1 if cromosoma[i] == 0 else 0
    return cromosoma

# Crear población inicial
def crear_población():
    return [[random.randint(0, 1) for _ in range(longitud_cromosoma)] for _ in range(tamaño_población)]

# Algoritmo Genético
def algoritmo_genetico():
    poblacion = crear_población()
    for generacion in range(max_generaciones):
        # Evaluar población
        poblacion = sorted(poblacion, key=fitness, reverse=True)
        mejor_cromosoma = poblacion[0]
        mejor_fitness = fitness(mejor_cromosoma)
        
        # Mostrar información de la generación actual con el cromosoma
        print(f"Generación {generacion + 1}: {mejor_cromosoma} (fitness = {mejor_fitness})")

        # Condición de parada: si encontramos un cromosoma con 20 unos
        if mejor_fitness == longitud_cromosoma:
            print(f"Convergencia alcanzada en la generación {generacion + 1}")
            break

        # Nueva generación
        nueva_poblacion = []
        
        # Elitismo: mantener el mejor cromosoma
        nueva_poblacion.append(mejor_cromosoma)
        
        # Selección, cruce y mutación
        while len(nueva_poblacion) < tamaño_población:
            padres = seleccion_ruleta(poblacion)
            hijo1, hijo2 = cruce(padres[0], padres[1])
            hijo1 = mutar(hijo1)
            hijo2 = mutar(hijo2)
            nueva_poblacion.append(hijo1)
            nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion[:tamaño_población]  # Asegurar que la población tiene el tamaño correcto

    return mejor_cromosoma

# Ejecutar algoritmo genético
resultado = algoritmo_genetico()
print("Cromosoma final:", resultado)
print("Fitness final:", fitness(resultado))
