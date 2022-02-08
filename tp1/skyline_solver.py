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

    def _divide_and_conquer(self, buildings):
        if len(buildings) <= 1:
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

    def dump_solution(self, output_file_path):
        self.skyline_parser.dump_critical_points(self.solution, output_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file", help="Input file with data", required=True, metavar="INPUT_FILE"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file to store results",
        required=True,
        metavar="OUTPUT_FILE",
    )

    args = parser.parse_args()

    skyline_solver = SkylineSolver()
    skyline_solver.load_data(args.file)
    skyline_solver.brute_force()
    # skyline_solver.divide_and_conquer()
    skyline_solver.dump_solution(args.output)
