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
    resultDyn = algo.dynamic(boxs)
    resultGlouton = algo.glouton(boxs)

    sumDyn = 0
    for res in resultDyn:
        sumDyn += res[0]


    sumGlout = 0
    for res in resultGlouton:
        sumGlout += res[0]

    #print("dynamic: ", resultDyn)
    #print("glouton: ", resultGlouton)
    print("dynamic height: ", sumDyn)
    print("glouton height: ", sumGlout)

    #algo.dynamic(boxs)
