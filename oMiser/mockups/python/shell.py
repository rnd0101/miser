import os
import readline
import atexit

from parsimonious import ParseError, VisitationError

import miser
from frugal import frugal_to_tree

readline.set_completer_delims(' \t\n')
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

histfile = os.path.join(os.path.expanduser("~"), ".frugal_history")
try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)

MISER_OBS = [item for item in dir(miser) if isinstance(getattr(miser, item), miser.ob)]


def completer(text, state):
    completions = ["." + o + " " for o in MISER_OBS if ("." + o).startswith(text)]
    if len(completions) == 0:
        return completions[0] + " "
    return completions[state]


readline.set_completer(completer)


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
        except (ParseError, VisitationError) as exc:
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
