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

def analyze_processing_times():
    """Compara tiempos de procesamiento secuencial y paralelo optimizado para diferentes cantidades de reseñas."""
    sequential_times = []

    for review_count in review_counts:
        # Procesamiento secuencial
        sequential_time = sum(item["time"] for item in processing_times[:review_count])  # Suma de tiempos de procesamiento secuencial
        sequential_times.append(sequential_time)

        print(f"Processed {review_count} reviews - Sequential")

    return sequential_times

def main():
    sequential_times = analyze_processing_times()

    # Almacenar los tiempos de procesamiento secuencial en un archivo CSV
    with open("Genetico_sequential.csv", "w") as file:
        file.write("review_count,time\n")
        for i, time in enumerate(sequential_times):
            file.write(f"{10000 * (i + 1)},{time}\n")

if __name__ == "__main__":
    main()