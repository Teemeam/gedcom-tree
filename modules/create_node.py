import pydot

# Create root child element node
def create_root_child_element_node(given_name, label, fillcolor):
    return pydot.Node(
        given_name,
        label=label,
        shape='box',
        style='filled',
        fontname='Arial',
        color=fillcolor,
        fillcolor=fillcolor
    )

# Create family node
def create_family_node(family):
    return pydot.Node(
        str(family),
        label='',
        shape='circle',
        fixedsize='true',
        width=0.1,
        height=0.1,
        style='filled',
        fillcolor='black'
    )