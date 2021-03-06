def graph_ob_structure(structure, level, prefix):
    name = "{}_{}".format(prefix, level)
    g = ""
    if type(structure) == tuple:
        if len(structure) == 2:
            g += """{} [shape=record,label="<f0> a|<f1> b"];\n""".format(name)
            sub_name, sub_g = graph_ob_structure(structure[0], level + 1, name + "a")
            g += sub_g + """{}:f0 -> {}:f0;\n""".format(name, sub_name)
            sub_name, sub_g = graph_ob_structure(structure[1], level + 1, name + "b")
            g += sub_g + """{}:f1 -> {}:f0;\n""".format(name, sub_name)
        else:
            g += """{} [shape=record,label="<f0> a"];\n""".format(name)
            sub_name, sub_g = graph_ob_structure(structure[0], level + 1, name + "a")
            g += sub_g + """{}:f0 -> {}:f0;\n""".format(name, sub_name)
    elif isinstance(structure, str):
        g += """{} [shape=record,label="<f0> {}"];\n""".format(name, structure)

    return (name, g)


def make_graph(obs, file_path):
    graph = """digraph ob {
    node [shape=record];
    """
    for (i, ob) in enumerate(obs):
        ob_structure = ob.__getstate__()
        _name, g = graph_ob_structure(ob_structure, 0, "ob{}_".format(i))
        graph += g

    graph += """}"""
    with open(file_path, "w") as f:
        print(graph, file=f)
