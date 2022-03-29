import argparse
import time
from Algo import Algo

if __name__ == "__main__":
    ######### INTERFACE #########
    algo = Algo()
    parser = argparse.ArgumentParser()

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
        "-e", "--sample", help="Sample path", required=True, metavar="SAMPLE"
    )

    parser.add_argument(
        "-p", "--print", help="Print results", required=False, action="store_true"
    )

    parser.add_argument(
        "-t", "--time", help="Print execution time", required=False, action="store_true"
    )

    args = parser.parse_args()

    algorithms = {
        "glouton": algo.glouton,
        "progdyn": algo.dynamic,
        "tabou": algo.taboo,
    }

    if args.algorithm not in algorithms:
        print("wrong algorithm:", args.algorithm)
    else:
        try:

            boxs = algo.parse_file(args.sample)
            solution = []

            if args.time:
                start = time.time()
                solution = algorithms[args.algorithm](boxs)
            else:
                solution = algorithms[args.algorithm](boxs)

            if args.print:
                algo.print(solution)
            if args.time:
                print('time', time.time() - start)
                print('size', algo.findH(solution))
                #algo.avrage(args.sample)
        except:
            pass



    
