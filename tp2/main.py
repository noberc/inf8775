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

    #algo.dynamic(boxs)
