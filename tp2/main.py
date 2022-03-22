import argparse
from glouton import Glouton

if __name__ == "__main__":
    glouton = Glouton()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file", help="Input file with data", required=True, metavar="INPUT_FILE"
    )

    args = parser.parse_args()

    boxs = glouton.parse_file(args.file)
    glouton.run(boxs)