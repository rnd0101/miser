import os
import readline
import atexit
from pprint import pprint

from parsimonious import ParseError, VisitationError

import miser
from frugal import frugal_to_tree
from graph import make_graph

DOT_FILE_PATH = "/tmp/omiser.dot"

readline.set_completer_delims(' \t\n')
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

shell_history_file = os.path.join(os.path.expanduser("~"), ".frugal_history")
try:
    readline.read_history_file(shell_history_file)
    readline.set_history_length(1000)
except IOError:
    pass
atexit.register(readline.write_history_file, shell_history_file)


def good_statement(s):
    if isinstance(s, miser.ob):
        return True
    return isinstance(s, tuple) and len(s) == 2 and isinstance(s[0], basestring) and isinstance(s[1], miser.ob)


def repl_loop(debug=True):
    print("oMiser/Frugal syntax interpreter")
    print("Press Ctrl-D to leave.")
    workspace = miser.namespace
    workspace.update({"cS": miser.cS})  # examples of variables

    def completer(text, state):
        if text.startswith("^"):
            completions = ["^" + o + " " for o in workspace
                           if not o.startswith(".") and not o.endswith("(") and ("^" + o).startswith(text)]
        else:
            completions = [o + " " for o in workspace if not o.endswith("(") and o.startswith(text)]
        if len(completions) == 0:
            return
        return completions[state]

    readline.set_completer(completer)

    while True:
        try:
            s = raw_input("\noMiser> ")
        except EOFError:
            print("\nBye!")
            break

        if not s.strip():
            continue
        graph = False
        if s.startswith("graph "):
            s = s[len("graph "):]
            graph = True
        try:
            statements = frugal_to_tree(s, workspace)
        except (ParseError, VisitationError) as exc:
            print("Parsing error: {}".format(exc))
            continue

        if not all(good_statement(x) for x in statements):
            print("ERROR: Ob expected, found: {}".format(statements))
            continue

        if graph:
            make_graph(statements, DOT_FILE_PATH)
            print("Graphviz file written to {}".format(DOT_FILE_PATH))
            continue

        for s in statements:
            to_var = None
            if isinstance(s, tuple):
                to_var, s = s
                print("ASSIGN INPUT: {} = {}".format(to_var, str(s)))
            else:
                print("INPUT: {}".format(str(s)))
            if to_var is not None:
                workspace[to_var] = s
                if debug:
                    pprint(workspace)
            else:
                evaluated = miser.eval(s)
                if debug:
                    print("INPUT: {}".format(repr(s)))
                    print("\nOUTPUT: {}".format(repr(evaluated)))
                print("OUTPUT: {}".format(str(evaluated)))
                if debug:
                    print("\nOUTPUT STATE: {}".format(repr(evaluated.__getstate__())))


if __name__ == "__main__":
    repl_loop()
