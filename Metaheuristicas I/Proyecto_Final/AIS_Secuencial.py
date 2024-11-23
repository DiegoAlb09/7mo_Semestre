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

# Análisis de tiempos secuenciales y paralelos optimizados
def analyze_processing_times_with_ais():
    sequential_times = []  # Almacena tiempos secuenciales
    
    for review_count in review_counts:
        # Procesamiento secuencial: suma de todos los tiempos de reseñas
        sequential_time = sum(item["time"] for item in processing_times[:review_count])
        sequential_times.append(sequential_time)
    
        print(f"Processed {review_count} reviews - Sequential: {sequential_time}")
    
    return sequential_times

def main():
    sequential_times = analyze_processing_times_with_ais()
    
    # Guardar los tiempos secuenciales en un archivo CSV
    with open("sequential_times.csv", "w") as file:
        file.write("review_count,time\n")
        for i, time in enumerate(sequential_times):
            file.write(f"{10000 * (i + 1)},{time}\n")

if __name__ == "__main__":
    main()