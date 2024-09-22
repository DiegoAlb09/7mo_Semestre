# Implementar el PSO para el problema de balance de carga
import numpy as np
import pyswarms as ps
import json
import matplotlib.pyplot as plt

# Cargar los datos del JSON
with open('Metaheuristicas I/reviews.json') as file:
    tasks = json.load(file)

# Extraer los tiempos de procesamiento de las tareas
processing_times = np.array([task['time'] for task in tasks])

# Numero de procesadores
num_processors = 8
numero_task = len(processing_times)

def fitness(task_assignment):
    task_assignment = np.array(task_assignment).astype(int)
    processor_loads = np.zeros(num_processors)
    if np.any(task_assignment < 0) or np.any(task_assignment >= num_processors):
        return np.inf
    for i, processor in enumerate(task_assignment):
        processor_loads[processor] += processing_times[i]
    return np.max(processor_loads)

# Limites del PSO (asignar tareas a procesadores de 0 a num_processors-1)
lower_bound = np.zeros(numero_task)
upper_bound = np.ones(numero_task) * (num_processors - 1)

# Ejecutar el algoritmo PSO
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=numero_task, options={'c1': 0.5, 'c2': 0.3, 'w':0.9})
best_assignment, best_fitness = optimizer.optimize(fitness, iters=50)
# Mostrar el resultado
print('Mejor asignación de tareas:', best_assignment)
print('Tiempo de procesamiento máximo en un procesador:', best_fitness)

# Graficar la asignación de tareas
plt.figure(figsize=(10, 5))
plt.bar(np.arange(numero_task), best_assignment)
plt.xlabel('Tarea')
plt.ylabel('Procesador')
plt.title('Asignación de tareas a procesadores')
plt.show()

# Graficar la carga de cada procesador (Presenta error)
#processor_loads = np.zeros(num_processors)
#for i, processor in enumerate(best_assignment):
#    processor_loads[int(processor)] += processing_times[i]
#plt.figure(figsize=(10, 5))
#plt.bar(np.arange(num_processors), processor_loads)
#plt.xlabel('Procesador')
#plt.ylabel('Tiempo de procesamiento')
#plt.title('Carga de cada procesador')
#plt.show()

#Tabla donde se compara el tiempo secuencia con el tiempo paralelo para 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000 y 10000 tareas
