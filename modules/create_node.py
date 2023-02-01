import pydot

# Import list of lineal descendants
import lineal_descendants

# Create root child element node
def create_root_child_element_node(given_name, label, pointer, fillcolor):

    # Create border for lineal descendants
    if pointer in lineal_descendants.lineal_descendants:
        return pydot.Node(
            given_name,
            label=label,
            shape='box',
            style='filled',
            fontname='Arial',
            color='#000000',
            penwidth=3,
            fillcolor=fillcolor
        )
    else:
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