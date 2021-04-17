import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", dest="outputs", nargs="+", help="Output files")
    args, rest = parser.parse_known_args()

    print("Building files {} from arguments {}".format(args.outputs, rest))
    for fname in args.outputs:
        with open(fname, "wt") as ofd:
            pass
