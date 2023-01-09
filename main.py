from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
import pydot

# Path
file_path = 'family_tree.ged'

# Initialize the parser
gedcom_parser = Parser()

# Parse the file
gedcom_parser.parse_file(file_path)

# Get the list of logical records in the file
root_child_elements = gedcom_parser.get_root_child_elements()

# Create the graph
graph = pydot.Dot(graph_type='graph', rankdir='BT', ranksep='2.0')

# Create an empty list to store the root child element nodes
root_child_element_nodes = []

# Iterate through all root child elements
for element in root_child_elements:

    # Check if `element` is an actual `IndividualElement`
    if isinstance(element, IndividualElement):

        # Get person data
        (given_name, surname) = element.get_name()
        birth_year = element.get_birth_year()
        death_year = element.get_death_year()
        gender = element.get_gender()

        # Create label
        label = ''
        if death_year == -1:
            label = given_name + ' ' + surname + '\ns. ' + str(birth_year)
        else:
            label = given_name + ' ' + surname + '\ns. ' + str(birth_year) + '\nk. ' + str(death_year)

        # Set fill color
        fillcolor = ''
        if gender == 'M':
            fillcolor = '#AFEEEE' # Pale turquoise
        else:
            fillcolor = '#FFE5B4' # Peach

        # Create node and add it to the graph
        root_child_element_node = pydot.Node(
            given_name,
            label=label,
            shape='box',
            style='filled',
            fontname='Arial',
            fillcolor=fillcolor
        )
        graph.add_node(root_child_element_node)
        root_child_element_nodes.append(root_child_element_node)

        # Get the parents of the current individual
        parents = gedcom_parser.get_parents(element)

        # Create an empty list to store the parent nodes
        parent_nodes = []

        # Add an edge between the current individual and each of their parents
        for parent in parents:

            # Check if `parent` is an actual `IndividualElement`
            if isinstance(parent, IndividualElement):

                # Get parent data
                (parent_given_name, parent_surname) = parent.get_name()

                # Create edges and add them to the graph
                parent_node = pydot.Node(parent_given_name, label=" ")
                graph.add_edge(pydot.Edge(root_child_element_node, parent_node, dir='back'))
                parent_nodes.append(parent_node)

# Write the graph
graph.write_png('build/family_tree.png')
graph.write_pdf('build/family_tree.pdf')