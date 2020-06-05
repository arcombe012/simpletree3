# cython: language_level=3
from functools import lru_cache         # pragma: no cover
from itertools import chain             # pragma: no cover


def reverse_path_iterator(node):
    """iterate through the parents of node until reaching root."""
    while node:
        yield node
        node = node.parent


def preorder_iterator(node):
    """preorder iteration of the tree nodes
    (first the node, then preorder through the children)"""
    yield node
    for child in node.children:
        yield from preorder_iterator(child)


def postorder_iterator(node):
    """postorder iteration of the tree nodes
    (first postorder through the children, then the node)"""
    for child in node.children:
        yield from postorder_iterator(child)
    yield node


def level_order_iterator(node):
    """level order iteration through the children"""
    nodes_ = [node]
    while len(nodes_):
        for node_ in nodes_:
            yield node_
        nodes_ = list(chain(*[node_.children for node_ in nodes_]))


def leaves_iterator(node):
    """iterate through the leaves (using preorder ordering)"""
    if 0 == node.children_count:
        yield node
    else:
        for child in node.children:
            yield from leaves_iterator(child)


def filtered_preorder_iterator(node, select=None, ignore=None):
    """selective preorder iteration
        - walk is preorder;
        - if select is specified, return the node if select(node) is True
        - if ignore is specified, skip completely the subtree rooted in node"""
    if ignore and ignore(node):
        return
    if select is None or select(node):
        yield node
    for child in node.children:
        yield from filtered_preorder_iterator(child, select, ignore)


def filtered_postorder_iterator(node, select=None, ignore=None):
    """selective postorder iteration
        - walk is postorder;
        - if select is specified, return the node if select(node) is True
        - if ignore is specified, skip completely the subtree rooted in node"""
    if ignore and ignore(node):
        return
    for child in node.children:
        yield from filtered_postorder_iterator(child, select, ignore)
    if select is None or select(node):
        yield node


def filtered_level_order_iterator(node, select=None, ignore=None):
    """selective level order iteration
        - walk is level order;
        - if select is specified, return the node if select(node) is True
        - if ignore is specified, skip completely the subtree rooted in node"""
    def _skip_node(n, skip=None):
        if skip and skip(n):
            return True
        return False
    if _skip_node(node, skip=ignore):       # pragma: no branch
        return
    nodes_ = [node]
    while len(nodes_):
        tmp_ = []
        for node_ in nodes_:
            if select is None or select(node_):       # pragma: no branch
                yield node_
            tmp_.extend(c for c in node_.children if not _skip_node(c, skip=ignore))
        nodes_ = tmp_


def filtered_leaves_iterator(node, select=None, ignore=None):
    """iterate through the leaves (using preorder ordering)"""
    if ignore and ignore(node):     # pragma: no branch
        return
    if 0 == node.children_count:
        if select is None or select(node):      # pragma: no branch
            yield node
    else:
        for child in node.children:
            yield from filtered_leaves_iterator(child, select, ignore)


def find_nodes(root_node, key):
    """preorder iterate through all the nodes in the tree with the given key,
    starting at the root"""
    if root_node.key == key:        # pragma: no branch
        yield root_node
    for child in root_node.children:
        yield from find_nodes(child, key)


@lru_cache()
def find_first_node(root_node, key):
    """find the first node in the tree (using preorder iteration) with the given key,
    starting at the root"""
    try:
        return next(find_nodes(root_node, key))
    except StopIteration:
        return None


def find_nodes_from_here(start_node, key):
    """preorder iterate through all the nodes in the tree with the given key,
    starting with the subtree rooted at the start node,
    then continuing with the parent's subtree, and so on until the total tree.
    Ensure that subtrees are walked only once.

    This is useful if there's reason to believe that
    often enough the nodes that are searched for are close to the start node"""
    node_ = start_node
    yield from find_nodes(node_, key)
    while node_.parent:
        this_key_ = node_.key
        node_ = node_.parent
        if node_.key == key:        # pragma: no branch
            yield node_
        for child_ in node_.children:
            if child_.key == this_key_:     # pragma: no branch
                continue
            yield from find_nodes(child_, key)


@lru_cache()
def find_first_node_from_here(start_node, key):
    """find the first node matching the tree,
    using the progressive subtree walking from the find_nodes_from_here iterator.

    Use it if the target node should probably be close to the starting one."""
    try:
        return next(find_nodes_from_here(start_node, key))
    except StopIteration:
        return None


def find_nodes_by_rule(root_node, select):
    """iterate through the nodes that match the select rule
    (a.k.a. select(node) == True"""
    if select(root_node):        # pragma: no branch
        yield root_node
    for child in root_node.children:
        yield from find_nodes_by_rule(child, select)


@lru_cache()
def find_first_node_by_rule(root_node, select):
    """find the first (in preorder) node that matches the select rule
    (a.k.a. select(node) == True"""
    try:
        return next(find_nodes_by_rule(root_node, select))
    except StopIteration:
        return None


def find_nodes_from_here_by_rule(start_node, select):
    """iterate through the nodes matching the select rule,
    using the progressive subtree walking"""
    node_ = start_node
    yield from find_nodes_by_rule(node_, select)
    while node_.parent:
        this_key_ = node_.key
        node_ = node_.parent
        if select(node_):        # pragma: no branch
            yield node_
        for child_ in node_.children:
            if child_.key == this_key_:     # pragma: no branch
                continue
            yield from find_nodes_by_rule(child_, select)


@lru_cache()
def find_first_node_from_here_by_rule(start_node, select):
    """find the first (in preorder) node that matches the select rule
    (a.k.a. select(node) == True
    using the progressive subtree walking"""
    try:
        return next(find_nodes_from_here_by_rule(start_node, select))
    except StopIteration:
        return None
