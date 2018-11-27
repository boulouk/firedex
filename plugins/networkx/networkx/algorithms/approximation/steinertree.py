from itertools import combinations, chain

from networkx.utils import pairwise, not_implemented_for
import networkx as nx

__all__ = ['metric_closure', 'steiner_tree']


@not_implemented_for('directed')
def metric_closure(G, relevant_nodes=None, weight='weight'):
    """  Return the metric closure of a graph. Optionally,
    it will only return the induced subgraph (of the metric
    closure) on the relevant_nodes.

    The metric closure of a graph *G* is the complete graph in which each edge
    is weighted by the shortest path distance between the nodes in *G* .

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    NetworkX graph
        Metric closure of the graph `G`.

    """
    M = nx.Graph()

    if relevant_nodes is None:
        relevant_nodes = G.nodes()
    # Because we assume undirected graphs, we'll only add path(u,v)
    # once and skip over path(v, u) or path (v, v)
    completed_nodes = set()
    relevant_nodes = set(relevant_nodes)

    # TODO: could skip over last node as well
    for u in relevant_nodes:
        # TODO: a proper metric closure might actually want self-loops,
        # so we'd need to remove the node from the set later on if so.
        completed_nodes.add(u)
        distance, path = nx.single_source_dijkstra(G, u, weight=weight)
        for v in relevant_nodes - completed_nodes:
            M.add_edge(u, v, distance=distance[v], path=path[v])

    # Original formulation did all pairs first, then induced subgraph,
    # which wastes a lot of time for most steiner_tree computations.
    # Furthermore, choosing the target specifically and iterating over
    # all combinations wastes time as well.
    # for u, v in combinations(G, 2):
    #     distance, path = nx.single_source_dijkstra(G, u, v, weight=weight)
    #     M.add_edge(u, v, distance=distance[v], path=path[v])

    return M


def steiner_tree(G, terminal_nodes, root=None, weight='weight'):
    """ Return an approximation to the minimum Steiner tree of a graph.

    Parameters
    ----------
    G : NetworkX graph

    terminal_nodes : list
         A list of terminal nodes for which minimum steiner tree is
         to be found.

    root : node
        Must be specified if G is directed

    Returns
    -------
    NetworkX graph
        Approximation to the minimum steiner tree of `G` induced by
        `terminal_nodes` and `root` (if specified).

    Notes
    -----
    UNDIRECTED GRAPHS:
    Steiner tree can be approximated by computing the minimum spanning
    tree of the subgraph of the metric closure of the graph induced by the
    terminal nodes, where the metric closure of *G* is the complete graph in
    which each edge is weighted by the shortest path distance between the
    nodes in *G* .
    This algorithm produces a tree whose weight is within a (2 - (2 / t))
    factor of the weight of the optimal Steiner tree where *t* is number of
    terminal nodes.

    DIRECTED GRAPHS:
    This is a generalization of the NP-hard Set Cover problem and so is known
    to be inapproximable within O(log(t)).  The simplest approximation is to
    join the shortest paths to each of the terminals, which approximates
    within t.  This is the approach this implementation takes.
    """
    if root is None:
        if G.is_directed():
            raise nx.NetworkXError("root must be specified for Steiner arborescence of digraphs!")
    elif not G.is_directed():
        terminal_nodes = terminal_nodes + [root]

    # TODO: enhance this algorithm for DiGraphs by taking the same metric closure approach.
    # However, this would require modifying the Edmonds algorithm / minimum_spanning_arborescence
    # implementations to accept an explicit root node.
    if G.is_directed():
        res = set()
        for term in terminal_nodes:
            path = nx.shortest_path(G, root, term, weight=weight)
            path_edges = zip(path, path[1:])
            for e in path_edges:
                res.add(e)
        res = G.edge_subgraph(e for e in res)

        assert all(t in res for t in terminal_nodes) and all(nx.has_path(res, root, t) for t in terminal_nodes)
        assert nx.is_directed_acyclic_graph(res)

        return res
    else:
        # M is the subgraph of the metric closure induced by the terminal nodes of
        # G.
        M = metric_closure(G, relevant_nodes=terminal_nodes, weight=weight)
        # Use the 'distance' attribute of each edge provided by the metric closure
        # graph.
        mst_edges = nx.minimum_spanning_edges(M, weight='distance', data=True)
        # Create an iterator over each edge in each shortest path; repeats are okay
        edges = chain.from_iterable(pairwise(d['path']) for u, v, d in mst_edges)
        T = G.edge_subgraph(edges)
        return T
