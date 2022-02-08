from skyline_solver import SkylineSolver
import pandas as pd
import glob
import timeit

class Profiler:

    def __init__(self, function):
        self.function = function

    def timed_run(self):
        samples_prefix = glob.glob("data/*_0")
        samples_prefix = [sample.split('_', 1)[0] for sample in samples_prefix]

        data = {'Taille': [int(prefix.split('N')[1]) for prefix in samples_prefix],
                'Naif': [],
                'DPR': []}

        for prefix in samples_prefix:
            samples = glob.glob(prefix + "_*")
            time = 0

            sample_size = int(prefix.split('N')[1])
            sample_len = 1

            for sample in samples:
                skyline_solver.load_data(sample)

                time += timeit.Timer(self.function).timeit(number=1)

                if sample_size >= 10000:
                    break

                sample_len = len(samples)

            data['Naif'].append(time / sample_len)

            print("brute force", sample_size, time / sample_len)
        # return time




skyline_solver = SkylineSolver()
profiler = Profiler(skyline_solver.brute_force)
profiler.timed_run()

# for index, prefix in enumerate(samples_prefix):
#     samples = glob.glob(prefix + "_*")
#     time = 0

#     sample_size = int(prefix.split('N')[1])
#     sample_len = len(samples)

#     for sample in samples:
#         skyline_solver.load_data(sample)

#         profiler = Profiler(skyline_solver.divide_and_conquer)
#         time += timeit.Timer(profiler.timed_run).timeit(number=1)

#     data['DPR'].append(time / sample_len)

#     print("brute force", sample_size, time / sample_len)


# df = pd.DataFrame(data)
# df.to_csv('results.csv')
