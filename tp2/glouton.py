
class Glouton:
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

        boxs = self.parse_boxs(self.opened_file)

        self.opened_file.close()

        return boxs

    def parse_boxs(self, input_data, from_file = True):
        boxs = []

        for box in input_data:
            
            if from_file:
                (l, p, h) = map(int, box.split())
            else:
                (l, p, h) = box

            boxs.append((l, p, h))

        return boxs

    def sortFunction(self, x):
        return x[0]


    def run(self, listBox):
        listBox.sort(key = self.sortFunction)
        listBox.reverse()
        sol = []
        sol.append(listBox[0])
        currentBox = sol[0]

        for box in listBox:
            if(box[0] < currentBox[0] and box[1] < currentBox[1]):
                sol.append(box)
                currentBox = box

        print(sol)
