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

    def should_elevate_point(self, critical_point, building):
        (cx, cy) = critical_point
        (bx1, bx2, by) = building

        return (bx1 <= cx < bx2) and (by > cy)

    def brute_force(self, output_file_path):

        if not len(self.buildings) or not len(self.critical_points):
            print("Load data first")
            return

        solution = []
        for (cx, cy) in self.critical_points:
            for (bx1, bx2, by) in self.buildings:
                if self.should_elevate_point((cx, cy), (bx1, bx2, by)):
                    cy = by

            list_empty = not len(solution)

            if list_empty or solution[-1][1] != cy:
                solution.append((cx, cy))

        self.skyline_parser.dump_critical_points(solution, output_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file",
                        help="Input file with data",
                        required=True,
                        metavar='INPUT_FILE')

    parser.add_argument("-o", "--output",
                        help="Output file to store results",
                        required=True,
                        metavar='OUTPUT_FILE')

    args = parser.parse_args()

    skyLineSolver = SkylineSolver()
    skyLineSolver.load_data(args.file)
    skyLineSolver.brute_force(args.output)
