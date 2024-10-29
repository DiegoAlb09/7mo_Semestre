import json
import numpy as np
import time
import pyswarms as ps

def read_json(file_path='reviews.json'):
  with open(file_path) as file:
    return json.load(file)
  
def process_window(tasks):
  return sum(tasks['time'] for tasks in tasks)

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
def measure_time(window_size, num_processors, max_reviews, tasks):
    pso_times = []
    review_counts = list(range(10000, max_reviews + 1, 10000))
    for count in review_counts:
        current_tasks = tasks[:count]
        start_time = time.time()
        pso_processing(current_tasks, window_size, num_processors)
        pso_times.append(time.time() - start_time)
        print(f"Processed {count} reviews")
    return pso_times

def main():
    window_size = 24
    num_processors = 8
    max_reviews = 100000
    tasks = read_json("reviews.json")
    pso_times = measure_time(window_size, num_processors, max_reviews, tasks)
    # Almacenar los tiempos de ejecución en un archivo csv
    with open("secuential_times.csv", "w") as file:
        file.write("review_count,time\n")
        for i, time in enumerate(pso_times):
            file.write(f"{10000 * (i + 1)},{time}\n")

if __name__ == "__main__":
    main()