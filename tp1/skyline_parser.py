class SkylineParser:
    def __init__(self):
        self.opened_file = None

    def open_file(self, input_file_path, permissions):
        try:
            self.opened_file = open(input_file_path, permissions)
        except OSError:
            print(f"OS error opening {input_file_path}")
            self.opened_file = None
        except FileNotFoundError:
            print(f"File {input_file_path} not found")
            self.opened_file = None
        except Exception as err:
            print(f"Unexpected error opening {input_file_path} is", repr(err))
            self.opened_file = None

    def parse_file(self, input_file_path):
        self.open_file(input_file_path, "r")

        if self.opened_file is None:
            print(f"Unexpected error opening {input_file_path}")
            return [], []

        next(self.opened_file)

        buildings, critical_points = self.parse_points(self.opened_file)

        self.opened_file.close()

        return buildings, critical_points

    def parse_points(self, input_data, from_file = True):

        buildings = []
        critical_points = []

        for line in input_data:
            if from_file:
                (x1, x2, y) = map(int, line.split())
            else:
                (x1, x2, y) = line

            buildings.append((x1, x2, y))
            critical_points.append((x1, y))
            critical_points.append((x2, 0))

        critical_points.sort()

        return buildings, critical_points

    def dump_critical_points(self, critical_points, output_file_path):

        self.open_file(output_file_path, "w+")

        if self.opened_file is None:
            print(f"Unexpected error opening {output_file_path}")
            return

        for line in critical_points:
            self.opened_file.write(" ".join(map(str, line)) + "\n")

    def print_critical_points(self, critical_points):
        for line in critical_points:
            print(" ".join(map(str, line)))
