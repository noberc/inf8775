import argparse

from skyline_parser import SkylineParser


class SkylineSolver:
    def __init__(self):
        self.skyline_parser = SkylineParser()
        self.critical_points = []
        self.buildings = []

    def load_data(self, input_file_path):
        if input_file_path is None:
            return

        (self.buildings, self.critical_points) = self.skyline_parser.parse_file(
            input_file_path
        )

    def _brute_force(self, buildings, critical_points):
        solution = []
        for (cx, cy) in critical_points:
            for (bx1, bx2, by) in buildings:
                if (bx1 <= cx < bx2) and (by > cy):
                    cy = by

            list_empty = not len(solution)

            if list_empty or solution[-1][1] != cy:
                solution.append((cx, cy))

        return solution

    def brute_force(self):

        if not len(self.buildings) or not len(self.critical_points):
            print("Load data first")
            return

        self.solution = self._brute_force(self.buildings, self.critical_points)

    def merge(self, critical_points1, critical_points2):

        solution = []

        h1 = h2 = h = 0
        i1 = i2 = 0

        while i1 < len(critical_points1) and i2 < len(critical_points2):

            (cx1, ch1) = critical_points1[i1]
            (cx2, ch2) = critical_points2[i2]

            if cx1 < cx2:
                h1 = ch1
            elif cx1 > cx2:
                h2 = ch2
            else:
                h1 = ch1
                h2 = ch2

            (x, h) = (min(cx1, cx2), max(h1, h2))

            list_empty = not len(solution)

            if list_empty or solution[-1][1] != h:
                solution.append((x, h))

            i1 += cx1 <= cx2
            i2 += cx2 <= cx1

        if i1 == len(critical_points1):
            solution.extend(critical_points2[i2:])
        else:
            solution.extend(critical_points1[i1:])
        return solution

    def _divide_and_conquer(self, buildings, treshold = 1):
        if len(buildings) <= treshold:
            _, critical_points = self.skyline_parser.parse_points(buildings, False)
            return self._brute_force(buildings, critical_points)

        half_index = len(buildings) // 2

        critical_points1 = self._divide_and_conquer(buildings[:half_index])
        critical_points2 = self._divide_and_conquer(buildings[half_index:])

        solution = self.merge(critical_points1, critical_points2)
        return solution

    def divide_and_conquer(self):
        if not len(self.buildings) or not len(self.critical_points):
            print("Load data first")
            return

        self.solution = self._divide_and_conquer(self.buildings)

    def divide_and_conquer_treshold(self):
        if not len(self.buildings) or not len(self.critical_points):
            print("Load data first")
            return

        self.solution = self._divide_and_conquer(self.buildings, 80)

    def dump_solution(self, output_file_path):
        self.skyline_parser.dump_critical_points(self.solution, output_file_path)

    def print_solution(self):
        self.skyline_parser.print_critical_points(self.solution)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file", help="Input file with data", required=False, metavar="INPUT_FILE"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file to store results",
        required=False,
        metavar="OUTPUT_FILE",
    )

    parser.add_argument(
        "-a",
        "--algorithm",
        help="The algorithm to use",
        required=True,
        metavar="ALGORITHM",
    )

    parser.add_argument(
        "-e",
        "--sample",
        help="Sample path",
        required=True,
        metavar="SAMPLE",
    )

    parser.add_argument(
        "-p",
        "--print",
        help="Print results",
        required=False,
        metavar="PRINT",
    )

    parser.add_argument(
        "-t",
        "--time",
        help="Print execution time",
        required=False,
        metavar="PRINT_EXECUTION",
    )

    args = parser.parse_args()

    skyline_solver = SkylineSolver()

    functions = {
        "brute": skyline_solver.brute_force,
        "recursif": skyline_solver.divide_and_conquer,
        "seuil": skyline_solver.divide_and_conquer_treshold,
    }

    if args.algorithm not in functions:
        print("wrong algorithm:", args.algorithm)
    else:
        try:
            skyline_solver.load_data(args.sample)
            functions[args.algorithm]()
            skyline_solver.print_solution()
        except:
            pass
