import plotly.express as px
from skyline_solver import SkylineSolver
import pandas as pd
import glob
import timeit

pd.set_option("display.max_columns", None)


class Profiler:
    def __init__(self, df=None):
        self.data = None
        self.df = df

    def timed_run(self, functions, samples_prefix, skyline_solver):

        self.data = {"Taille": [int(prefix.split("N")[1]) for prefix in samples_prefix]}

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

        self.df = pd.DataFrame(self.data).sort_values("Taille")
        self.df.to_csv("results.csv")
        print(self.df)

        # return time

    def load_data(self, df):
        if df is None:
            return

        self.df = df

    def plot_data(self):
        if self.df is None:
            return

        fig = px.scatter(
            self.df,
            x="Taille",
            y=["Naif", "DPR", "DPRS"],
            log_x=True,
            log_y=True,
            trendline="ols",
            trendline_options=dict(log_x=True, log_y=True),
        )

        model = px.get_trendline_results(fig)
        alpha = model.iloc[0]["px_fit_results"].params[0]
        beta = model.iloc[0]["px_fit_results"].params[1]

        fig.data[1].name = ' y = ' + str(round(alpha, 2)) + ' + ' + str(round(beta, 2)) + 'x'
        fig.data[1].showlegend = True

        alpha = model.iloc[1]["px_fit_results"].params[0]
        beta = model.iloc[1]["px_fit_results"].params[1]

        fig.data[3].name = ' y = ' + str(round(alpha, 2)) + ' + ' + str(round(beta, 2)) + 'x'
        fig.data[3].showlegend = True

        alpha = model.iloc[2]["px_fit_results"].params[0]
        beta = model.iloc[2]["px_fit_results"].params[1]

        fig.data[5].name = ' y = ' + str(round(alpha, 2)) + ' + ' + str(round(beta, 2)) + 'x'
        fig.data[5].showlegend = True
        fig.show()


def compute_average_times(profiler):
    skyline_solver = SkylineSolver()
    samples_prefix = glob.glob("data/*_0")
    samples_prefix = [sample.split("_", 1)[0] for sample in samples_prefix]

    functions = {
        "Naif": skyline_solver.brute_force,
        "DPR": skyline_solver.divide_and_conquer,
        "DPRS": skyline_solver.divide_and_conquer_treshold,
    }

    profiler.timed_run(functions, samples_prefix, skyline_solver)


def plot_times(profiler, df=None):
    if df is None:
        compute_average_times(profiler)
        profiler.plot_data()
    else:
        profiler.load_data(df)
        profiler.plot_data()

profiler = Profiler()
# compute_average_times(profiler)
plot_times(profiler, pd.read_csv('results.csv'))
