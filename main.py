from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
import pydot
from tqdm import tqdm

# Import modules
from modules.create_node import create_root_child_element_node, create_family_node
from modules.add import add_node, add_edge

# Path
file_path = 'family_tree.ged'

# Initialize the parser
gedcom_parser = Parser()

# Parse the file
gedcom_parser.parse_file(file_path)

# Get the list of logical records in the file
root_child_elements = gedcom_parser.get_root_child_elements()

# Create the graph
graph = pydot.Dot(graph_type='graph', rankdir='TB', ranksep='1.0')

# Create an empty list to store the root child element nodes
root_child_element_nodes = set()

# Create an empty list to store the family nodes
family_nodes = set()

# Create an empty set to store the parent edges
parent_edges = set()

# Create an empty set to store the child edges
child_edges = set()

# Iterate through all root child elements
for element in tqdm(root_child_elements, desc='Iterating: '):

    # Check if `element` is an actual `IndividualElement`
    if isinstance(element, IndividualElement):

        # Get individual data
        (given_name, surname) = element.get_name()
        birth_year = element.get_birth_year()
        death_year = element.get_death_year()
        gender = element.get_gender()
        pointer = element.get_pointer()

        # Create label
        label = f'{ given_name } { surname }'
        if birth_year != -1:
            label += f'\n* { birth_year }'
        if death_year != -1:
            label += f'\n+ { death_year }'

        # Set fill color
        fillcolor = ''
        if gender == 'M':
            fillcolor = '#D9D77F' # Men
        elif gender == 'F':
            fillcolor = '#E4BEA4' # Women
        else:
            fillcolor = '#EEEEEE' # Unknown

        # Create a new node for the current individual
        root_child_element_node = create_root_child_element_node(pointer, label, fillcolor)

        # Check if the current root child element node has already been added to the graph
        if root_child_element_node not in root_child_element_nodes:

            # Add the newly created root child element node to the graph and the list of root child element nodes
            add_node(graph, root_child_element_node, root_child_element_nodes)

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
                pointer = parent.get_pointer()

                # Create a new node for the current parent
                parent_node = pydot.Node(pointer, label='')

                # Add the current parent node to the list of parent nodes. Not used currently.
                parent_nodes.append(parent_node)

                # Get a list of families that the current parent is a part of
                families = gedcom_parser.get_families(parent)

                # Iterate through each of the families found in the previous step
                for family in families:

                    # Create a new node for the current family
                    family_node = create_family_node(family)

                    # Check if the current family node has already been added to the graph
                    if family_node not in family_nodes:

                        # Add the family node to the graph and the list of family nodes
                        add_node(graph, family_node, family_nodes)

                    # Create an edge between the current parent node and the current family node
                    parent_edge = pydot.Edge(parent_node, family_node)

                    # Check if the current parent edge has already been added to the graph
                    if parent_edge not in parent_edges:

                        # Add the parent edge to the graph and the list of parent edges
                        add_edge(graph, parent_edge, parent_edges)

                    # Get a list of family members that the current family has
                    family_members = gedcom_parser.get_family_members(family)

                    # Check if the current element is in the list of family members of the current family
                    if element in family_members:

                        # Create an edge between the current family node and the current child node
                        child_edge = pydot.Edge(family_node, root_child_element_node, dir='forward')

                        # Check if the current child edge has already been added to the graph
                        if child_edge not in child_edges:

                            # Add the child edge to the graph and the list of child edges
                            add_edge(graph, child_edge, child_edges)

                # In addition to families of individuals and their parents, get the families of individuals and their children
                families = gedcom_parser.get_families(element)

                # Iterate through each of the families found in the previous step
                for family in families:

                    # Create a new node for the current family
                    family_node = create_family_node(family)

                    # Check if the current family node has already been added to the graph
                    if family_node not in family_nodes:

                        # Add the family node to the graph and the list of family nodes
                        add_node(graph, family_node, family_nodes)

                    # Create an edge between the current parent node and the current family node
                    parent_edge = pydot.Edge(root_child_element_node, family_node)

                    # Check if the current parent edge has already been added to the graph
                    if parent_edge not in parent_edges:

                        # Add the parent edge to the graph and the list of parent edges
                        add_edge(graph, parent_edge, parent_edges)

        # If the current individual has no parents or they are unknown
        if not parents:

            # Get a list of families that the current individual is a part of
            families = gedcom_parser.get_families(element)

            # Iterate through each of the families found in the previous step
            for family in families:

                # Create a new node for the current family
                family_node = create_family_node(family)

                # Check if the current family node has already been added to the graph
                if family_node not in family_nodes:

                    # Add the family node to the graph and the list of family nodes
                    add_node(graph, family_node, family_nodes)

                # Create an edge between the current parent node and the current family node
                parent_edge = pydot.Edge(root_child_element_node, family_node)

                # Check if the current parent edge has already been added to the graph
                if parent_edge not in parent_edges:

                    # Add the parent edge to the graph and the list of parent edges
                    add_edge(graph, parent_edge, parent_edges)

# Write the graph
graph.write_png('build/family_tree.png')
graph.write_pdf('build/family_tree.pdf')