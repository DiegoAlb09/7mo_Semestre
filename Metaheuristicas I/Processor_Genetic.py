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

def genetic_algorithm(window_times):
    """Ejecuta el algoritmo genético para optimizar la asignación de tareas en una ventana."""
    population = toolbox.population(n=population_size)  # Crea una población inicial
    
    # Define la función de evaluación para esta ejecución
    def evaluate_individual(individual):
        return fitness(individual, window_times)
    
    toolbox.register("evaluate", evaluate_individual)  # Actualiza la función de evaluación en el toolbox
    
    # Imprime la población inicial antes de comenzar las generaciones
    #print("Población inicial:")
    #for i, ind in enumerate(population):
        #print(f"Individuo {i}: {ind}")

    # Calcula la aptitud (fitness) de la población inicial
    for ind in population:
        ind.fitness.values = toolbox.evaluate(ind)
    
    # Ejecuta el algoritmo genético con la función de evaluación actualizada
    algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=num_generations, verbose=False)
    
    best_individual = tools.selBest(population, k=1)[0]  # Selecciona el mejor individuo de la población final
    return best_individual, fitness(best_individual, window_times)[0]  # Retorna el mejor individuo y su tiempo óptimo

def analyze_processing_times():
    """Compara tiempos de procesamiento secuencial y paralelo optimizado para diferentes cantidades de reseñas."""
    sequential_times = []
    parallel_times = []

    for review_count in review_counts:
        # Procesamiento secuencial
        sequential_time = sum(item["time"] for item in processing_times[:review_count])  # Suma de tiempos de procesamiento secuencial
        sequential_times.append(sequential_time)

        # Procesamiento paralelo optimizado con Algoritmo Genético
        total_parallel_time = 0
        for i in range(0, review_count, window_size):
            window_times = [item["time"] for item in processing_times[i:i+window_size]]  # Extrae tiempos de procesamiento en la ventana actual
            _, optimal_time = genetic_algorithm(window_times)  # Ejecuta el algoritmo genético para optimizar la ventana
            total_parallel_time += optimal_time  # Suma el tiempo óptimo de la ventana al tiempo total
        parallel_times.append(total_parallel_time)

        print(f"{review_count} reviews - Sequential: {sequential_time}, Optimized Parallel: {total_parallel_time}")

    return sequential_times, parallel_times

# Ejecuta el análisis y gráfica los resultados
sequential_times, parallel_times = analyze_processing_times()

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
