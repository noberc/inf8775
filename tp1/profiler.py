import os
from skyline_solver import SkylineSolver
import glob
import timeit

class Profiler:

    def __init__(self, function):
        self.function = function

    def timed_run(self):
         self.function()


skyline_solver = SkylineSolver()
samples = os.listdir("data/")
for sample in samples:
    file_path = "data/" + sample

    skyline_solver.load_data(file_path)

    profiler = Profiler(skyline_solver.brute_force)
    print("brute force", sample, timeit.Timer(profiler.timed_run).timeit(number=1))
