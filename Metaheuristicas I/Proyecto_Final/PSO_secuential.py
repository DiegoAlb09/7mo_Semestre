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
  return sum(tasks['time'] for tasks in tasks)

def measure_times(tasks, window_size, num_processors, max_reviews):
  sequential_times = []
  review_counts = list(range(10000, max_reviews + 1, 10000))

  for count in review_counts:
    current_tasks = tasks[:count]

    sequential_time = sum(task['time'] for task in current_tasks)
    sequential_times.append(sequential_time)
    print(f"Processed {count} reviews")

  return sequential_times

def main():
  window_size = 100
  num_processors = 8
  max_reviews = 100000
  tasks = read_json("reviews.json")
  sequential_times = measure_times(tasks, window_size, num_processors, max_reviews)

  with open("PSO_sequential.csv", "w") as file:
    file.write("review_count,time\n")
    for i, time in enumerate(sequential_times):
      file.write(f"{10000 * (i + 1)},{time}\n")

if __name__ == "__main__":
  main()
