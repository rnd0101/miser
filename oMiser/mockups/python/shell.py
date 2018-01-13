from parsimonious import ParseError

import miser
from frugal import frugal_to_tree


def repl_loop(debug=False):
    print("oMiser/Frugal syntax interpreter")
    print("Press Ctrl-D to leave.")
    while True:
        try:
            s = raw_input("\noMiser> ")
        except EOFError:
            print("\nBye!")
            break

        try:
            s = frugal_to_tree(s, miser)
        except ParseError as exc:
            print("Parsing error: {}".format(exc))
            continue
        if not isinstance(s, miser.ob):
            print("ERROR: Ob expected")
            continue
        if debug:
            print("INPUT: {}".format(repr(s)))
            print("\nOUTPUT: {}".format(repr(miser.eval(s))))
        print("INPUT: {}".format(str(s)))
        print("\nOUTPUT: {}".format(str(miser.eval(s))))


if __name__ == "__main__":
    repl_loop()
