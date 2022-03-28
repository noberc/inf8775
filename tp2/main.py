import argparse
from Algo import Algo

if __name__ == "__main__":
    ######### INTERFACE #########
    # algo = Algo()
    # parser = argparse.ArgumentParser()

    # parser.add_argument(
    #     "-o",
    #     "--output",
    #     help="Output file to store results",
    #     required=False,
    #     metavar="OUTPUT_FILE",
    # )

    # parser.add_argument(
    #     "-a",
    #     "--algorithm",
    #     help="The algorithm to use",
    #     required=True,
    #     metavar="ALGORITHM",
    # )

    # parser.add_argument(
    #     "-e", "--sample", help="Sample path", required=True, metavar="SAMPLE"
    # )

    # parser.add_argument(
    #     "-p", "--print", help="Print results", required=False, action="store_true"
    # )

    # parser.add_argument(
    #     "-t", "--time", help="Print execution time", required=False, action="store_true"
    # )

    # args = parser.parse_args()

    # algorithms = {
    #     "glouton": algo.glouton,
    #     "progdyn": algo.dynamic,
    #     "tabou": algo.taboo,
    # }

    # if args.algorithm not in algorithms:
    #     print("wrong algorithm:", args.algorithm)
    # else:
    #     try:

    #         boxs = algo.parse_file(args.sample)
    #         solution = []
    #         time = 0

    #         if args.time:
    #             # TODO
    #             # time = timeit.Timer(algorithms[args.algorithm]).timeit(number=1) * 1000
    #             solution = algorithms[args.algorithm](boxs)
    #         else:
    #             solution = algorithms[args.algorithm](boxs)

    #         if args.print:
    #             algo.print(solution)
    #         if args.time:
    #             print(time)
    #     except:
    #         pass



    ######### A ENLEVER #########
    algo = Algo()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file", help="Input file with data", required=True, metavar="INPUT_FILE"
    )

    args = parser.parse_args()

    boxs = algo.parse_file(args.file)
    resultDyn = algo.dynamic(boxs.copy())
    resultGlouton = algo.glouton(boxs.copy())
    resultTaboo = algo.taboo(boxs.copy())

    sumDyn = algo.findH(resultDyn)
    sumGlout = algo.findH(resultGlouton)
    sumTaboo = algo.findH(resultTaboo)

    print("---------")
    print("dynamic: ", resultDyn)
    print("---------")
    print("glouton: ", resultGlouton)
    print("---------")
    print("taboo: ", resultTaboo)
    print("---------")
    print("dynamic height: ", sumDyn)
    print("glouton height: ", sumGlout)
    print("taboo height: ", sumTaboo)

    # algo.dynamic(boxs)
    ######### A ENLEVER #########
