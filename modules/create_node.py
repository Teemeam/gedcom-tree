import pydot

# Import list of lineal descendants
from modules.lineal_descendants import lineal_descendants

# Create root child element node
def create_root_child_element_node(pointer, label, fillcolor):

    # Lineal descendants have darker background
    if pointer in lineal_descendants:
        return pydot.Node(
            pointer,
            label=label,
            shape='box',
            style='filled',
            fontname='Arial',
            color=fillcolor,
            fillcolor=fillcolor
        )
    else:
        return pydot.Node(
            pointer,
            label=label,
            shape='box',
            style='filled',
            fontname='Arial',
            color=f'{ fillcolor }4D', # 30 %
            fillcolor=f'{ fillcolor }4D' # 30 %
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