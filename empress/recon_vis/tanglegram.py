"""
tanglegram.py
Visualizes tanglegrams using matplotlib
Berto Garcia, Sonia Sehra
"""

from empress.recon_vis import utils, plot_tools

VERTICAL_OFFSET = 20
HORIZONTAL_SPACING = 10
LEAF_SPACING = 5
HOST_COUNTER = 0
PARASITE_COUNTER = 0

def render(host_dict: dict, parasite_dict: dict, phi: dict, show_internal_labels: bool) -> None:
    """
    Render tanglegram
    :param host_dict - host tree (dictionary representation)
    :param parasite_dict - parasite tree (dictionary representation)
    :param phi - tip mapping dictionary
    :param show_internal_labels - boolean indicator of whether internal node names should
        be displayed
    :return FigureWrapper object 
    """
    fig = plot_tools.FigureWrapper("Host | Parasite")
    host_tree = utils.dict_to_tree(host_dict, tree.TreeType.HOST)
    parasite_tree = utils.dict_to_tree(parasite_dict, tree.TreeType.PARASITE)
    render_helper_host(fig, host_tree.root_node, show_internal_labels)
    render_helper_parasite(fig, parasite_tree.root_node, show_internal_labels)

    host_dict = {}
    for host in host_tree.leaf_list():
        host_dict[host.name] = host

    # connect hosts leaves to parasite leaves
    for leaf in parasite_tree.leaf_list():
        parasite = leaf
        host = host_dict[phi[leaf.name]]
        fig.line((host.layout.col, host.layout.row), (parasite.layout.col, parasite.layout.row),
                 col=plot_tools.GRAY, style='--')
    return fig

def render_helper_host(fig, node, show_internal_labels):
    """
    Render helper for host tree
    """
    global HOST_COUNTER
    if node.is_leaf:

        # set up layout for node (will be used later for drawing lines between nodes)
        leaf_layout = tree.NodeLayout()
        leaf_layout.col = -VERTICAL_OFFSET
        leaf_layout.row = HOST_COUNTER

        HOST_COUNTER += LEAF_SPACING
        node.layout = leaf_layout

        # plot node using leaf_layout
        plot_loc = (leaf_layout.col, leaf_layout.row)
        fig.text(plot_loc, node.name, col=plot_tools.BLUE, h_a='left')

    else:
        # recursively call helper funciton on child nodes
        render_helper_host(fig, node.left_node, show_internal_labels)
        render_helper_host(fig, node.right_node, show_internal_labels)

        # get layouts for child nodes to determine position of current node
        right_layout = node.right_node.layout
        left_layout = node.left_node.layout

        # create layout for current node
        node.layout = tree.NodeLayout()
        node.layout.col = min(right_layout.col, left_layout.col) - HORIZONTAL_SPACING
        y_avg = (float(right_layout.row)+float(left_layout.row))/2.0
        node.layout.row = y_avg

        # plot node using node_layout
        current_loc = (node.layout.col, node.layout.row)
        if show_internal_labels:
            fig.text(current_loc, node.name, col=plot_tools.BLUE, h_a='left')

        # draw line from current node to left node
        left_loc = (left_layout.col, left_layout.row)
        fig.line(current_loc, (node.layout.col, left_layout.row), col=plot_tools.BLACK)
        fig.line((node.layout.col, left_layout.row), left_loc, col=plot_tools.BLACK)

        # draw line from current node to right node
        right_loc = (right_layout.col, right_layout.row)
        fig.line(current_loc, (node.layout.col, right_layout.row), col=plot_tools.BLACK)
        fig.line((node.layout.col, right_layout.row), right_loc, col=plot_tools.BLACK)


def render_helper_parasite(fig, node, show_internal_labels):
    """
    Render helper for parasite tree
    """

    global PARASITE_COUNTER
    if node.is_leaf:
        # set up layout for node (will be used later for drawing lines between nodes)
        leaf_layout = tree.NodeLayout()
        leaf_layout.col = VERTICAL_OFFSET
        leaf_layout.row = PARASITE_COUNTER

        PARASITE_COUNTER += LEAF_SPACING
        node.layout = leaf_layout

        # plot node using leaf_layout
        plot_loc = (leaf_layout.col, leaf_layout.row)
        fig.text(plot_loc, node.name, col=plot_tools.BLUE, h_a='right')

    else:
        # recursively call helper funciton on child nodes
        render_helper_parasite(fig, node.left_node, show_internal_labels)
        render_helper_parasite(fig, node.right_node, show_internal_labels)

        # get layouts for child nodes to determine position of current node
        right_layout = node.right_node.layout
        left_layout = node.left_node.layout

        # create layout for current node
        node.layout = tree.NodeLayout()
        node.layout.col = max(left_layout.col, right_layout.col) + HORIZONTAL_SPACING
        y_avg = (float(right_layout.row)+float(left_layout.row))/2.0
        node.layout.row = y_avg

        # plot node using node_layout
        current_loc = (node.layout.col, node.layout.row)
        if show_internal_labels:
            fig.text(current_loc, node.name, col=plot_tools.BLUE, h_a='right')

        # draw line from current node to left node
        left_loc = (left_layout.col, left_layout.row)
        fig.line(current_loc, (node.layout.col, left_layout.row), col=plot_tools.BLACK)
        fig.line((node.layout.col, left_layout.row), left_loc, col=plot_tools.BLACK)

        # draw line from current node to right node
        right_loc = (right_layout.col, right_layout.row)
        fig.line(current_loc, (node.layout.col, right_layout.row), col=plot_tools.BLACK)
        fig.line((node.layout.col, right_layout.row), right_loc, col=plot_tools.BLACK)

