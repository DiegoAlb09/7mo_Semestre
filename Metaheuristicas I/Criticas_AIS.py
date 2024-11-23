# Importación de librerías necesarias
import json
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
from deap import base, creator, tools, algorithms

# Cargar datos JSON con los tiempos de procesamiento de reseñas de películas
with open('reviews.json') as f:
    processing_times = json.load(f)  # Lista de tiempos de procesamiento para cada reseña

# Parámetros generales del problema
num_processors = 8                     # Número de procesadores disponibles para distribuir las tareas
window_size = 100                      # Tamaño de las ventanas deslizantes (100 reseñas por ventana)
population_size = 50                   # Tamaño de la población en el algoritmo genético
num_generations = 100                  # Número de generaciones en el algoritmo genético
review_counts = [10000, 20000, 30000,  # Lista con cantidades de reseñas para analizar el rendimiento
                 40000, 50000, 60000,
                 70000, 80000, 90000, 100000]

# Configuración de DEAP para el algoritmo genético
# Se crean las clases necesarias para individuos y fitness
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Clase para minimizar el tiempo de procesamiento máximo
creator.create("Individual", list, fitness=creator.FitnessMin)  # Clase que representa a un individuo como una lista

# Configuración de operadores del algoritmo genético
toolbox = base.Toolbox()
toolbox.register("attr_processor", random.randint, 0, num_processors - 1)  # Atributo: procesador aleatorio (0 a 7)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_processor, n=window_size)  # Crear un individuo
toolbox.register("population", tools.initRepeat, list, toolbox.individual)  # Crear una población de individuos

# Función de fitness: calcula el tiempo máximo de procesamiento entre procesadores para un individuo
def fitness(individual, times):
    processor_times = [0] * num_processors  # Inicializa tiempos de los procesadores
    for task_index, processor in enumerate(individual):  # Asigna tareas a procesadores
        processor_times[processor] += times[task_index]  # Suma el tiempo de cada tarea al procesador correspondiente
    return max(processor_times),  # Devuelve el tiempo máximo, ya que es el valor que queremos minimizar

# Registro de la función de fitness y operadores genéticos en el toolbox
toolbox.register("evaluate", fitness)  # Registra la función de evaluación
toolbox.register("mate", tools.cxUniform, indpb=0.5)  # Cruce uniforme con probabilidad de intercambio del 50%
toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)  # Mutación: invierte el procesador asignado con probabilidad del 10%
toolbox.register("select", tools.selRoulette)  # Selección por ruleta (probabilidad proporcional al fitness)

# Parámetros para el Sistema Inmunológico Artificial (AIS)
memory_size = 10  # Número de soluciones óptimas (anticuerpos) a mantener en memoria
clone_factor = 5  # Número de clones generados por cada anticuerpo

# Inicialización de la memoria de anticuerpos
antibody_memory = []  # Lista para almacenar las mejores soluciones encontradas

# Función para actualizar la memoria de anticuerpos con una nueva solución
def update_memory(new_individual, window_times):
    new_fitness = fitness(new_individual, window_times)[0]
    # Si la memoria está vacía o la nueva solución es mejor que la peor en la memoria
    if len(antibody_memory) < memory_size or new_fitness < max(fitness(antibody, window_times)[0] for antibody in antibody_memory):
        antibody_memory.append(new_individual)  # Agregar la nueva solución
        antibody_memory.sort(key=lambda ind: fitness(ind, window_times)[0])  # Ordenar por fitness
        if len(antibody_memory) > memory_size:  # Si la memoria excede el tamaño permitido
            antibody_memory.pop()  # Eliminar el peor anticuerpo

# Función para clonar y mutar un anticuerpo, generando diversidad en las soluciones
def clone_and_mutate(antibody):
    clones = []
    for _ in range(clone_factor):  # Generar clones
        clone = toolbox.clone(antibody)  # Crear una copia del anticuerpo
        toolbox.mutate(clone)  # Aplicar mutación al clon
        clones.append(clone)  # Agregar a la lista de clones
    return clones

# Implementación del Algoritmo Genético combinado con AIS
def genetic_algorithm_with_ais(window_times):
    population = toolbox.population(n=population_size)  # Inicializa la población
    for ind in population:  # Evalúa la población inicial
        ind.fitness.values = fitness(ind, window_times)
    
    for gen in range(num_generations):  # Para cada generación
        # Actualizar memoria de anticuerpos con soluciones de la población
        for ind in population:
            if ind.fitness.values < (fitness(antibody_memory[-1], window_times) if antibody_memory else (float('inf'),)):
                update_memory(ind, window_times)
        
        # Generar clones de los anticuerpos y agregarlos a la población
        clones = [clone for antibody in antibody_memory for clone in clone_and_mutate(antibody)]
        population.extend(clones)  # Añadir clones a la población
        
        # Selección, cruce y mutación
        offspring = toolbox.select(population, k=population_size)  # Selección de la siguiente generación
        offspring = list(map(toolbox.clone, offspring))  # Clonar la población seleccionada
        
        for child1, child2 in zip(offspring[::2], offspring[1::2]):  # Aplicar operadores genéticos
            if random.random() < 0.5:  # Probabilidad de cruce
                toolbox.mate(child1, child2)
            toolbox.mutate(child1)  # Aplicar mutación
            toolbox.mutate(child2)
            child1.fitness.values = fitness(child1, window_times)  # Recalcular fitness
            child2.fitness.values = fitness(child2, window_times)
        
        population[:] = offspring  # Reemplazar la población con la nueva generación
    
    best_individual = tools.selBest(population, k=1)[0]  # Seleccionar el mejor individuo
    return best_individual, fitness(best_individual, window_times)[0]  # Retornar el mejor individuo y su fitness

# Análisis de tiempos secuenciales y paralelos optimizados
def analyze_processing_times_with_ais():
    sequential_times = []  # Almacena tiempos secuenciales
    parallel_times = []    # Almacena tiempos paralelos optimizados
    
    for review_count in review_counts:
        # Procesamiento secuencial: suma de todos los tiempos de reseñas
        sequential_time = sum(item["time"] for item in processing_times[:review_count])
        sequential_times.append(sequential_time)
        
        # Procesamiento paralelo optimizado
        total_parallel_time = 0
        for i in range(0, review_count, window_size):  # Dividir en ventanas
            window_times = [item["time"] for item in processing_times[i:i+window_size]]  # Tiempos de la ventana
            _, optimal_time = genetic_algorithm_with_ais(window_times)  # Ejecutar GA+AIS
            total_parallel_time += optimal_time  # Sumar el tiempo paralelo de la ventana
        parallel_times.append(total_parallel_time)
    
        print(f"{review_count} reviews - Sequential: {sequential_time}, Optimized Parallel: {total_parallel_time}")
    
    return sequential_times, parallel_times

# Ejecuta el análisis con AIS y gráfica los resultados
sequential_times, parallel_times = analyze_processing_times_with_ais()

# Gráfico de resultados (líneas)
plt.figure(figsize=(10, 6))
plt.plot(review_counts, sequential_times, label='Sequential Processing Time')
plt.plot(review_counts, parallel_times, label='Optimized Parallel Processing Time')
plt.xlabel('Number of Reviews')
plt.ylabel('Processing Time (s)')
plt.title('Sequential vs Optimized Parallel Processing Time')
plt.legend()
plt.show()

# Gráfico de resultados (barras)
plt.figure(figsize=(10, 6))
barWidth = 0.3
r1 = np.arange(len(review_counts))
r2 = [x + barWidth for x in r1]
plt.bar(r1, sequential_times, color='b', width=barWidth, edgecolor='grey', label='Sequential Processing Time')
plt.bar(r2, parallel_times, color='r', width=barWidth, edgecolor='grey', label='Optimized Parallel Processing Time')
plt.xlabel('Number of Reviews')
plt.ylabel('Processing Time (s)')
plt.title('Sequential vs Optimized Parallel Processing Time')
plt.xticks([r + barWidth for r in range(len(review_counts))], review_counts)
plt.legend()
plt.show()

# Tabla de resultados y porcentajes de mejora
speedup = [sequential / parallel for sequential, parallel in zip(sequential_times, parallel_times)]  # Relación de mejora
percent = [(1 - parallel/sequential) * 100 for sequential, parallel in zip(sequential_times, parallel_times)]  # Porcentaje de mejora

# Mostrar tabla de resultados
df = pd.DataFrame({
    'Number of Reviews': review_counts, 
    'Sequential Time': sequential_times, 
    'Parallel Time': parallel_times, 
    'Speedup': speedup, 
    'Improvement (%)': percent
})
print(df)
