def add_node(graph, node, nodes):
    
    # Add node to the graph
    graph.add_node(node)

    # Add the node to the list of nodes
    nodes.add(node)

def add_edge(graph, edge, edges):
    
    # Add edge to the graph
    graph.add_edge(edge)

    # Add the edge to the list of edges
    edges.add(edge)