from skyline_solver import SkylineSolver
import timeit

class Profiler:

    def __init__(self, function):
        self.function = function

    def timed_run(self):
         self.function()

skyline_solver = SkylineSolver()
skyline_solver.load_data("data/N10000_0")
profiler = Profiler(skyline_solver.brute_force)
print(timeit.Timer(profiler.timed_run).timeit(number=1))
