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

def parallel_processing(tasks, window_size, num_processors):
    with mp.Pool(num_processors) as pool:
        total_time = 0
        for i in range(0, len(tasks), window_size * num_processors):
            windows = [tasks[i + j * window_size : i + (j + 1) * window_size] for j in range(num_processors)]
            window_times = pool.map(process_window, windows)
            total_time += max(window_times)
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
    optimizer = ps.single.GlobalBestPSO(n_particles=100, dimensions=num_tasks, options=options, bounds=bounds)
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
    pso_times = []
    review_counts = list(range(10000, max_reviews + 1, 10000))
    

    for count in review_counts:
        current_tasks = tasks[:count]

        start_time = time.time()
        parallel_processing(current_tasks, window_size, num_processors)
        pso_times.append((time.time() - start_time) * 10)

        sequential_time = sum(task['time'] for task in current_tasks)
        sequential_times.append(sequential_time)


    return review_counts, sequential_times, pso_times

def plot_results(review_counts, sequential_times, pso_times):
    plt.figure(figsize=(12, 8))
    plt.plot(review_counts, sequential_times, label='Sequential', marker='o')
    plt.plot(review_counts, pso_times, label='Parallel', marker='o')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Processing Time (s)')
    plt.title('Movie Review Processing Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('PSO.png')
    plt.show()

def main():
    window_size = 100
    num_processors = 8
    max_reviews = 100000

    tasks = read_json("reviews.json")
    review_counts, sequential_times, pso_times = measure_times(tasks, window_size, num_processors, max_reviews)
    plot_results(review_counts, sequential_times, pso_times)

    speedup = [sequential_times / pso_times for sequential_times, pso_times in zip(sequential_times, pso_times)]
    percent = [(1 - pso / sequential) * 100 for pso, sequential in zip(pso_times, sequential_times)]
    df = pd.DataFrame({
    'Number of Reviews': review_counts,  
    'Sequential Time': sequential_times, 
    'Parallel Time': pso_times,
    'Speedup': speedup,
    'Improvement (%)': percent
    })
    print(df)

if __name__ == '__main__':
    main()
