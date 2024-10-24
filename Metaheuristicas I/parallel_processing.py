import multiprocessing as mp
import time
import json

def read_json(file_path='reviews.json'):
  with open(file_path) as file:
    return json.load(file)
  
def process_window(tasks):
  return sum(tasks['time'] for tasks in tasks)

def parallel_processing(tasks, window_size, num_processors):
  total_time = 0
  try:
    with mp.Pool(num_processors) as pool:
      for i in range(0, len(tasks), window_size * num_processors):
        windows = [tasks[i + j * window_size: i + (j + 1) * window_size] for j in range(num_processors)]
        window_times = pool.map(process_window, windows)
        total_time += max(window_times)
        print(f"Processed {i + window_size} reviews")
  except Exception as e:
    print(f"Error during parallel processing: {e}")
  return total_time

def measure_time(window_size, num_processors, max_reviews, tasks):
  parallel_times = []
  review_counts = list(range(10000, max_reviews + 1, 10000))
  for counts in review_counts:
    current_tasks = tasks[:counts]
    start_time = time.time()
    parallel_processing(current_tasks, window_size, num_processors)
    parallel_times.append(time.time() - start_time)
    print(f"Processed {counts} reviews in {parallel_times[-1]} seconds")
  return parallel_times

def main():
  window_size = 1000
  num_processors = 8
  max_reviews = 100000
  tasks = read_json("reviews.json")
  parallel_times = measure_time(window_size, num_processors, max_reviews, tasks)
  # Almacenar los tiempos de ejecución en un archivo csv
  with open("parallel_times.csv", "w") as file:
    file.write("review_count,time\n")
    for i, time in enumerate(parallel_times):
      file.write(f"{10000 * (i + 1)},{time}\n")

if __name__ == "__main__":
  main()