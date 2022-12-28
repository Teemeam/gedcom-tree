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
        (first, last) = element.get_name()
        root_child_element_node = pydot.Node(first, label=first + " " + last)
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
                (first_parent, last_parent) = parent.get_name()
                parent_node = pydot.Node(first_parent, label=first_parent + " " + last_parent)
                graph.add_edge(pydot.Edge(root_child_element_node, parent_node))
                parent_nodes.append(parent_node)

graph.write_png('family_tree.png')