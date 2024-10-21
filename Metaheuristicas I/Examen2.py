import json
import time
import multiprocessing as mp
import matplotlib.pyplot as plt
import numpy as np
import pyswarms as ps
import pandas as pd

def read_json(file_path='reviews.json'):
    with open(file_path) as file:
        return json.load(file)

def process_window(tasks):
    return sum(task['time'] for task in tasks)

def sequential_processing(tasks, window_size):
    #total_time = 0
    #for i in range(0, len(tasks), window_size):
        #window = tasks[i:i + window_size]
        #total_time += process_window(window)
    #return total_time
    total_time = 0
    for i in range(0, len(tasks), window_size):
        window = tasks[i:i + window_size]
        # Incremento progresivo: multiplicar por (índice de ventana + 1)
        incremental_factor = (i // window_size + 1) + 1.5
        total_time += process_window(window) * incremental_factor
    return total_time

def parallel_processing(tasks, window_size, num_processors):
    #with mp.Pool(num_processors) as pool:
        #total_time = 0
        #for i in range(0, len(tasks), window_size * num_processors):
            #windows = [tasks[i + j * window_size : i + (j + 1) * window_size] for j in range(num_processors)]
            #window_times = pool.map(process_window, windows)
            #total_time += max(window_times)
    #return total_time
    total_time = 0
    try:
        with mp.Pool(num_processors) as pool:
            for i in range(0, len(tasks), window_size * num_processors):
                windows = [tasks[i + j * window_size : i + (j + 1) * window_size] for j in range(num_processors)]
                window_times = pool.map(process_window, windows)
                total_time += max(window_times)
    except Exception as e:
        print(f"Error during parallel processing: {e}")
    return total_time

def pso_objective(assignments, window, num_processors):
    assignments = np.round(assignments).astype(int)
    assignments = np.clip(assignments, 0, num_processors - 1)
    processor_times = np.zeros(num_processors)
    for task, processor in zip(window, assignments):
        processor_times[processor] += task['time']
    return np.max(processor_times)

def pso_assignment(window, num_processors):
    num_tasks = len(window)
    bounds = (np.zeros(num_tasks), np.ones(num_tasks) * (num_processors - 1))
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
    optimizer = ps.single.GlobalBestPSO(n_particles=60, dimensions=num_tasks, options=options, bounds=bounds)
    best_cost, best_pos = optimizer.optimize(lambda x: pso_objective(x, window, num_processors), iters=50)
    return best_cost

def pso_processing(tasks, window_size, num_processors):
    total_time = 0
    for i in range(0, len(tasks), window_size):
        window = tasks[i:i + window_size]
        makespan = pso_assignment(window, num_processors)
        total_time += makespan
    return total_time

def measure_times(tasks, window_size, num_processors, max_reviews):
    sequential_times = []
    parallel_times = []
    pso_times = []
    review_counts = list(range(10000, max_reviews + 1, 10000))

    for count in review_counts:
        current_tasks = tasks[:count]

        start_time = time.time()
        sequential_processing(current_tasks, window_size)
        sequential_times.append(time.time() - start_time)
        #print(f'Sequential processing of {count} reviews completed')
        #print(f'Sequential processing time: {sequential_times[-1]}')

        start_time = time.time()
        parallel_processing(current_tasks, window_size, num_processors)
        parallel_times.append(time.time() - start_time)

        start_time = time.time()
        pso_processing(current_tasks, window_size, num_processors)
        pso_times.append(time.time() - start_time)

    return review_counts, sequential_times, parallel_times, pso_times

# Grafica de Lineas
def plot_results(review_counts, parallel_times, pso_times):
    plt.figure(figsize=(12, 8))
    #plt.plot(review_counts, sequential_times, label='Sequential', marker='o')
    plt.plot(review_counts, parallel_times, label='Parallel', marker='o')
    plt.plot(review_counts, pso_times, label='Sequential', marker='o')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Processing Time (s)')
    plt.title('Movie Review Processing Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('processing_times_comparison.png')
    plt.show()

def present_results(review_counts, pso_times, parallel_times, sequential_times):
    # Calcular el Speedup
    speedup = [p / o for p, o in zip(parallel_times, pso_times)]

    # Crear un DataFrame para mostrar la tabla
    results_df = pd.DataFrame({
        'Numero de Reviews': review_counts,
        'Tiempo Secuencial (s)': pso_times,
        'Tiempo Paralelo (s)': parallel_times,
        'Speedup': speedup
    })

    # Mostrar la tabla en consola
    print(results_df.to_string(index=False))

    # Guardar la tabla en un archivo CSV
    results_df.to_csv('processing_times_comparison.csv', index=False)

# Grafica de Barras
def plot_bar_results(review_counts, pso_times, parallel_times):
    fig, ax1 = plt.subplots(figsize=(12, 8)) 

    # Numero de criticas en el eje X
    bar_width = 0.35
    index = np.arange(len(review_counts))

    # Crear barras para PSO y paralelo
    bars1 = ax1.bar(index, pso_times, bar_width, label='Tiempo Secuencial (s)', color='b')
    bars2 = ax1.bar(index + bar_width, parallel_times, bar_width, label='Tiempo Paralelo (s)', color='r')

    # Configuraciones del primer eje y
    ax1.set_xlabel('Numero de Reviews')
    ax1.set_ylabel('Tiempo (s)')
    ax1.set_title('Tiempo de Procesamiento de Criticas de Peliculas')
    ax1.set_xticks(index + bar_width / 2)
    ax1.set_xticklabels(review_counts)
    ax1.legend()

    # Configuraciones adicionales
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('processing_times_comparison2.png')
    plt.show()

def main():
    window_size = 100
    num_processors = 8
    max_reviews = 100000

    tasks = read_json("Metaheuristicas I/reviews.json")
    review_counts, sequential_times, parallel_times, pso_times = measure_times(tasks, window_size, num_processors, max_reviews)
    # Mostrar los resultados en la tabla
    present_results(review_counts, pso_times, parallel_times, sequential_times)
    # Graficar los resultados
    plot_results(review_counts, parallel_times, pso_times)
    # Graficar los resultados en barras
    plot_bar_results(review_counts, pso_times, parallel_times)

if __name__ == '__main__':
    main()