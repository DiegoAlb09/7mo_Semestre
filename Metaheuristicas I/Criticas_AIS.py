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
    processing_times = json.load(f)

# Parámetros
num_processors = 8                     # Número de procesadores disponibles para la asignación de tareas
window_size = 100                      # Tamaño de la ventana deslizante (cantidad de reseñas procesadas en cada ventana)
population_size = 50                   # Tamaño de la población para el algoritmo genético
num_generations = 100                  # Número de generaciones en el algoritmo genético
review_counts = [10000, 20000, 30000,  # Lista con cantidades de reseñas para probar el rendimiento del algoritmo
                 40000, 50000, 60000,
                 70000, 80000, 90000, 100000]

# Configuración de DEAP para el algoritmo genético
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Crear una clase de fitness para minimizar el tiempo
creator.create("Individual", list, fitness=creator.FitnessMin)  # Crear una clase de individuos (soluciones)

# Inicialización de cada tarea en un individuo como una asignación de procesador (0 a num_processors - 1)
toolbox = base.Toolbox()
toolbox.register("attr_processor", random.randint, 0, num_processors - 1)  # Procesador aleatorio entre 0 y 7
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_processor, n=window_size)  # Crear un individuo con asignaciones aleatorias de procesador para cada tarea
toolbox.register("population", tools.initRepeat, list, toolbox.individual)  # Crear una población de individuos

def fitness(individual, times):
    """Calcula el tiempo máximo de procesamiento entre todos los procesadores para una asignación dada."""
    processor_times = [0] * num_processors  # Inicializa los tiempos de procesamiento para cada procesador
    for task_index, processor in enumerate(individual):
        processor_times[processor] += times[task_index]  # Acumula el tiempo de cada tarea en el procesador asignado
    return max(processor_times),  # Devuelve el tiempo máximo (el objetivo es minimizar este valor)

toolbox.register("evaluate", fitness)  # Registra la función de evaluación en el toolbox
toolbox.register("mate", tools.cxUniform, indpb=0.5)  # Cruce uniforme con una probabilidad de 0.5
toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)  # Mutación que invierte el procesador asignado con probabilidad de 0.1
toolbox.register("select", tools.selRoulette)  # Selección de individuos usando ruleta

# Parámetros para el sistema inmune artificial
memory_size = 10  # Número de soluciones óptimas (anticuerpos) almacenadas
clone_factor = 5  # Número de clones para cada anticuerpo

# Inicializar la memoria de anticuerpos (soluciones de alta calidad)
antibody_memory = []

def update_memory(new_individual, window_times):
    """
    Actualiza la memoria de anticuerpos con una nueva solución si es mejor.
    """
    new_fitness = fitness(new_individual, window_times)[0]
    # Revisar si la memoria está llena y si la nueva solución es mejor que las almacenadas
    if len(antibody_memory) < memory_size or new_fitness < max(fitness(antibody, window_times)[0] for antibody in antibody_memory):
        # Añadir y ordenar la memoria, manteniendo solo los mejores anticuerpos
        antibody_memory.append(new_individual)
        antibody_memory.sort(key=lambda ind: fitness(ind, window_times)[0])
        if len(antibody_memory) > memory_size:
            antibody_memory.pop()  # Eliminar el peor anticuerpo si se excede el tamaño

def clone_and_mutate(antibody):
    """
    Clona un anticuerpo y aplica mutación para crear diversidad.
    """
    clones = []
    for _ in range(clone_factor):
        clone = toolbox.clone(antibody)
        toolbox.mutate(clone)  # Aplicar mutación
        clones.append(clone)
    return clones

def genetic_algorithm_with_ais(window_times):
    """
    Ejecuta el algoritmo genético optimizado con el sistema inmune artificial (AIS).
    """
    population = toolbox.population(n=population_size)
    for ind in population:
        ind.fitness.values = fitness(ind, window_times)
    
    for gen in range(num_generations):
        # Evaluar población y actualizar memoria de anticuerpos
        for ind in population:
            if ind.fitness.values < (fitness(antibody_memory[-1], window_times) if antibody_memory else (float('inf'),)):
                update_memory(ind, window_times)
        
        # Crear clones de los anticuerpos y añadirlos a la población
        clones = [clone for antibody in antibody_memory for clone in clone_and_mutate(antibody)]
        population.extend(clones)
        
        # Selección, cruce y mutación en la población extendida
        offspring = toolbox.select(population, k=population_size)
        offspring = list(map(toolbox.clone, offspring))
        
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:
                toolbox.mate(child1, child2)
            toolbox.mutate(child1)
            toolbox.mutate(child2)
            child1.fitness.values = fitness(child1, window_times)
            child2.fitness.values = fitness(child2, window_times)
        
        population[:] = offspring
    
    best_individual = tools.selBest(population, k=1)[0]
    return best_individual, fitness(best_individual, window_times)[0]

# Reemplazar el algoritmo genético en analyze_processing_times con AIS
def analyze_processing_times_with_ais():
    sequential_times = []
    parallel_times = []
    
    for review_count in review_counts:
        # Procesamiento secuencial
        sequential_time = sum(item["time"] for item in processing_times[:review_count])
        sequential_times.append(sequential_time)
        
        # Procesamiento paralelo optimizado con Algoritmo Genético + AIS
        total_parallel_time = 0
        for i in range(0, review_count, window_size):
            window_times = [item["time"] for item in processing_times[i:i+window_size]]
            _, optimal_time = genetic_algorithm_with_ais(window_times)
            total_parallel_time += optimal_time
        parallel_times.append(total_parallel_time)
    
        print(f"{review_count} reviews - Sequential: {sequential_time}, Optimized Parallel: {total_parallel_time}")
    
    return sequential_times, parallel_times

# Ejecuta el análisis con AIS y gráfica los resultados
sequential_times, parallel_times = analyze_processing_times_with_ais()

# Gráfico de Resultados
plt.figure(figsize=(10, 6))
plt.plot(review_counts, sequential_times, label='Sequential Processing Time')
plt.plot(review_counts, parallel_times, label='Optimized Parallel Processing Time')
plt.xlabel('Number of Reviews')
plt.ylabel('Processing Time (s)')
plt.title('Sequential vs Optimized Parallel Processing Time')
plt.legend()
plt.show()

# Gráfico de barras
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
speedup = [sequential / parallel for sequential, parallel in zip(sequential_times, parallel_times)]
percent = [(1 - parallel/sequential) * 100 for sequential, parallel in zip(sequential_times, parallel_times)]

# Dataframe con los resultados de la comparación y el porcentaje de mejora
df = pd.DataFrame({
    'Number of Reviews': review_counts, 
    'Sequential Time': sequential_times, 
    'Parallel Time': parallel_times, 
    'Speedup': speedup, 
    'Improvement (%)': percent
})
print(df)
