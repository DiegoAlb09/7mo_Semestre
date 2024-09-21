import unittest
import numpy as np
from PSO_Exam import fitness, processing_times, num_processors

class TestPSOExam(unittest.TestCase):

  def setUp(self):
    # Setup any necessary data here
    self.processing_times = processing_times
    self.num_processors = num_processors

  def test_fitness(self):
    # Test with a valid task assignment
    task_assignment = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    result = fitness(task_assignment)
    self.assertIsInstance(result, float, "The result should be a float")
    
    # Test with an invalid task assignment (out of bounds)
    task_assignment = np.array([0, 1, 2, 3, 4, 5, 6, 8])
    with self.assertRaises(IndexError):
      fitness(task_assignment)
    
    # Test with an empty task assignment
    task_assignment = np.array([])
    result = fitness(task_assignment)
    self.assertEqual(result, 0, "The result should be 0 for an empty task assignment")

if __name__ == '__main__':
  unittest.main()