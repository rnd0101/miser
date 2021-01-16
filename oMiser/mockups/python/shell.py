import argparse
import os
import readline
import atexit
from pprint import pprint

from lark import UnexpectedCharacters
from parsimonious import ParseError, VisitationError
from ofrugal_grammar import parser as ofrugal_parser, Interpretation

import miser
import library
from frugal import frugal_to_tree, Command, Equation
from graph import make_graph
from solve import solve

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
    return isinstance(s, tuple) and len(s) == 2 and isinstance(s[0], str) and isinstance(s[1], miser.ob)


def repl_loop(modules, debug=False, do_eval=False):
    print("oFrugal shell for oMiser computational model")
    print("Press Ctrl-D to leave.")
    workspace = miser.namespace
    workspace.update(library.namespace)

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
        line = None
        while len(modules) > 0:
            line = modules[0].readline()
            if line:
                break
            to_close = modules.pop(0)
            print(("Read: {}".format(to_close.name)))
            to_close.close()

        if line:
            s = line
        else:
            try:
                s = input("\noFrugal> ")
            except EOFError:
                print("\nBye!")
                break

        if not s.strip():
            continue

        try:
            parsed = ofrugal_parser.parse(s)
        except UnexpectedCharacters as x:
            print("\nParser error:", x)
            continue
        else:
            # print (parsed)  # TODO: properly integrate into shell
            pass
        I = Interpretation(workspace)
        # print((I(parsed)))

        try:
            statements = frugal_to_tree(s, workspace)
        except (ParseError, VisitationError) as exc:
            print(("Parsing error: {}".format(exc)))
            continue

        graph = False
        if isinstance(statements, Command):
            if statements.name == "include":
                file_name = statements.arguments.strip('"')
                try:
                    modules.append(open(file_name, "r"))
                except IOError as x:
                    print(("ERROR: {}".format(x)))
                continue
            elif statements.name == "debug":
                debug = not debug
                print(("Debug now {}".format(["OFF", "ON"][debug])))
                continue
            elif statements.name == "eval":
                do_eval = not do_eval
                print(("Implicit eval now {}".format(["OFF", "ON"][do_eval])))
                continue
            elif statements.name == "graph":
                graph = True
                if not statements.arguments.strip():
                    print("Empty input.")
                    continue
                statements = frugal_to_tree(statements.arguments, workspace)
        elif isinstance(statements[0], Equation):
            if len(set(eq.varname for eq in statements)) != 1:
                print("ERROR: different variables")
                continue
            varname = statements[0].varname
            rules = [(eq.args, eq.result) for eq in statements]
            try:
                solutions = solve(rules)
            except TypeError as x:
                print("\nInternal error:", x)
                continue
            except KeyboardInterrupt:
                print("Aborted.")
                continue
            if solutions:
                workspace[varname] = solutions[-1]
                if debug:
                    pprint(workspace)
            else:
                print("No solution found, more calculations needed.")
            continue

        if not all(good_statement(x) for x in statements):
            print(("ERROR: Ob expected, found: {}".format(statements)))
            continue

        if graph:
            make_graph(statements, DOT_FILE_PATH)
            print(("Graphviz file written to {}".format(DOT_FILE_PATH)))
            continue

        for s in statements:
            to_var = None
            if isinstance(s, tuple):
                to_var, s = s
                print(("{} = {}".format(to_var, str(s))))
            if to_var is not None:
                workspace[to_var] = s
                if debug:
                    pprint(workspace)
            else:
                if do_eval:
                    evaluated = miser.eval(s)
                else:
                    evaluated = s
                print(("{}".format(str(evaluated))))
                if debug:
                    print(("\nOUTPUT: {}".format(repr(evaluated))))
                    print(("\nOUTPUT STATE: {}".format(repr(evaluated.__getstate__()))))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='oFrugal shell.')
    parser.add_argument('modules', metavar='M', type=argparse.FileType('r'), nargs='*')
    args = parser.parse_args()

    repl_loop(args.modules)
