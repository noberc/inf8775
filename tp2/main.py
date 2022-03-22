import argparse
from Algo import Algo

if __name__ == "__main__":
    algo = Algo()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file", help="Input file with data", required=True, metavar="INPUT_FILE"
    )

    args = parser.parse_args()

    boxs = algo.parse_file(args.file)
    print(algo.glouton(boxs))
    algo.taboo(boxs)
    #algo.dynamic(boxs)