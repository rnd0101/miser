import miser
from frugal import frugal_to_tree


# print(frugal_to_tree('.C', miser))

def repl_loop():
    print("oMiser/Frugal syntax interpreter")
    print("Press Ctrl-D to leave.")
    while True:
        try:
            s = raw_input("\noMiser> ")
        except EOFError:
            print("\nBye!")
            break

        s = frugal_to_tree(s, miser)
        if not isinstance(s, miser.ob):
            print("ERROR: Ob expected")
            continue
        print("INPUT: {}".format(repr(s)))
        print("ABBR: {}".format(str(s)))
        print("\nOUTPUT: {}".format(repr(miser.eval(s))))


if __name__ == "__main__":
    repl_loop()
