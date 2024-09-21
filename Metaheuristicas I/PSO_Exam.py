# Implementar el PSO para el problema de balance de carga
import numpy as np
import pyswarms as ps
import json

# Cargar los datos del JSON
with open('Metaheuristicas I/reviews.json') as file:
    tasks = json.load(file)

# Extraer los tiempos de procesamiento de las tareas
processing_times = np.array([task['time'] for task in tasks])

# Numero de procesadores
num_processors = 8
numero_task = len(processing_times)

# Función fitness para minimizar el tiempo de procesamiento
#def fitness(task_assignment):
    #processor_loads = np.zeros(num_processors)
    #for i in range(task_assignment):
        #processor_loads[i] += processing_times[i]
    #return np.max(processor_loads)
#print(fitness(8))
def fitness(task_assignment):
    processor_loads = np.zeros(num_processors)
    for i, processor in enumerate(task_assignment):
        processor_loads[processor] += processing_times[i] #arrays used as indices must be of integer (or boolean) type
    return np.max(processor_loads)


# Limites del PSO (asignar tareas a procesadores de 0 a num_processors-1)
lower_bound = np.zeros(numero_task)
upper_bound = np.ones(numero_task) * (num_processors - 1)

# Ejecutar el algoritmo PSO
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=numero_task, options={'c1': 0.5, 'c2': 0.3, 'w':0.9})
best_assignment, best_fitness = optimizer.optimize(fitness, iters=1000)
# Mostrar el resultado
print('Mejor asignación de tareas:', best_assignment)
print('Tiempo de procesamiento máximo en un procesador:', best_fitness)