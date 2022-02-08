from skyline_solver import SkylineSolver
import pandas as pd
import glob
import timeit

pd.set_option('display.max_columns', None)

class Profiler:

    def __init__(self, df = None):
        self.data = None
        self.df = df

    def timed_run(self, functions, samples_prefix, skyline_solver):

        self.data = {'Taille': [int(prefix.split('N')[1]) for prefix in samples_prefix]}

        for name, function in functions.items():

            self.data[name] = []

            for prefix in samples_prefix:
                samples = glob.glob(prefix + "_*")
                time = 0

                sample_len = 1

                for sample in samples:
                    skyline_solver.load_data(sample)

                    time += timeit.Timer(function).timeit(number=1)

                    sample_len = len(samples)

                self.data[name].append(time / sample_len)

        self.df = pd.DataFrame(self.data).sort_values('Taille')
        self.df.to_csv('results.csv')
        print(self.df)

        # return time




def compute_average_times():
    skyline_solver = SkylineSolver()
    samples_prefix = glob.glob("data/*_0")
    samples_prefix = [sample.split('_', 1)[0] for sample in samples_prefix]

    functions = {'Naif': skyline_solver.brute_force,
                 'DPR': skyline_solver.divide_and_conquer}

    profiler = Profiler()
    profiler.timed_run(functions, samples_prefix, skyline_solver)


# compute_average_times()
