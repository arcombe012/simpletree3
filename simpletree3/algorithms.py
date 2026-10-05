from collections import deque
from collections.abc import Callable, Generator, Hashable

from .abstract_node import AbstractNode

# All the walks below are iterative (explicit stack/queue), so that
# deep trees do not hit the recursion limit and each yielded node
# costs O(1) instead of O(depth) nested generator frames.


def reverse_path_iterator(node: AbstractNode | None) -> Generator[AbstractNode, None, None]:
    """iterate through the parents of node until reaching root."""
    n_ = node
    while n_ is not None:
        yield n_
        n_ = n_.parent


def preorder_iterator(node: AbstractNode) -> Generator[AbstractNode, None, None]:
    """preorder iteration of the tree nodes
    (first the node, then preorder through the children)"""
    stack_ = [node]
    while stack_:
        n_ = stack_.pop()
        yield n_
        stack_.extend(reversed(list(n_.children)))


def postorder_iterator(node: AbstractNode) -> Generator[AbstractNode, None, None]:
    """postorder iteration of the tree nodes
    (first postorder through the children, then the node)"""
    stack_: list[tuple[AbstractNode, bool]] = [(node, False)]
    while stack_:
        n_, expanded_ = stack_.pop()
        if expanded_:
            yield n_
        else:
            stack_.append((n_, True))
            stack_.extend((c_, False) for c_ in reversed(list(n_.children)))


def level_order_iterator(node: AbstractNode) -> Generator[AbstractNode, None, None]:
    """level order iteration through the children"""
    queue_ = deque([node])
    while queue_:
        n_ = queue_.popleft()
        yield n_
        queue_.extend(n_.children)


def leaves_iterator(node: AbstractNode) -> Generator[AbstractNode, None, None]:
    """iterate through the leaves (using preorder ordering)"""
    for n_ in preorder_iterator(node):
        if n_.children_count == 0:
            yield n_


def filtered_preorder_iterator(node: AbstractNode,
        select: Callable[[AbstractNode], bool] | None = None,
        ignore: Callable[[AbstractNode], bool] | None = None) \
        -> Generator[AbstractNode, None, None]:
    """selective preorder iteration
        - walk is preorder;
        - if select is specified, return the node if select(node) is True
        - if ignore is specified, skip completely the subtree rooted in node"""
    stack_ = [node]
    while stack_:
        n_ = stack_.pop()
        if ignore is not None and ignore(n_):
            continue
        if select is None or select(n_):
            yield n_
        stack_.extend(reversed(list(n_.children)))


def filtered_postorder_iterator(node: AbstractNode,
        select: Callable[[AbstractNode], bool] | None = None,
        ignore: Callable[[AbstractNode], bool] | None = None)\
        -> Generator[AbstractNode, None, None]:
    """selective postorder iteration
        - walk is postorder;
        - if select is specified, return the node if select(node) is True
        - if ignore is specified, skip completely the subtree rooted in node"""
    stack_: list[tuple[AbstractNode, bool]] = [(node, False)]
    while stack_:
        n_, expanded_ = stack_.pop()
        if expanded_:
            if select is None or select(n_):
                yield n_
        elif ignore is None or not ignore(n_):
            stack_.append((n_, True))
            stack_.extend((c_, False) for c_ in reversed(list(n_.children)))


def filtered_level_order_iterator(node: AbstractNode,
        select: Callable[[AbstractNode], bool] | None = None,
        ignore: Callable[[AbstractNode], bool] | None = None)\
        -> Generator[AbstractNode, None, None]:
    """selective level order iteration
        - walk is level order;
        - if select is specified, return the node if select(node) is True
        - if ignore is specified, skip completely the subtree rooted in node"""
    queue_ = deque([node])
    while queue_:
        n_ = queue_.popleft()
        if ignore is not None and ignore(n_):
            continue
        if select is None or select(n_):
            yield n_
        queue_.extend(n_.children)


def filtered_leaves_iterator(node: AbstractNode,
        select: Callable[[AbstractNode], bool] | None = None,
        ignore: Callable[[AbstractNode], bool] | None = None)\
        -> Generator[AbstractNode, None, None]:
    """iterate through the leaves (using preorder ordering)
        - if select is specified, return the leaf if select(leaf) is True
        - if ignore is specified, skip completely the subtree rooted in node"""
    for n_ in filtered_preorder_iterator(node, ignore=ignore):
        if n_.children_count == 0 and (select is None or select(n_)):
            yield n_


def count_nodes(node: AbstractNode) -> int:
    """return the number of nodes in the subtree rooted in node (including node)"""
    return sum(1 for _ in preorder_iterator(node))


def lowest_common_ancestor(node_a: AbstractNode, node_b: AbstractNode) -> AbstractNode | None:
    """return the deepest node that is an ancestor of (or equal to) both nodes,
    or None if they belong to different trees"""
    ancestors_a_ = {id(n_) for n_ in reverse_path_iterator(node_a)}
    for n_ in reverse_path_iterator(node_b):
        if id(n_) in ancestors_a_:
            return n_
    return None


def find_nodes(root_node: AbstractNode, key: Hashable) -> Generator[AbstractNode, None, None]:
    """preorder iterate through all the nodes in the tree with the given key,
    starting at the root"""
    return find_nodes_by_rule(root_node, lambda n_: n_.key == key)


def find_first_node(root_node: AbstractNode, key: Hashable) -> AbstractNode | None:
    """find the first node in the tree (using preorder iteration) with the given key,
    starting at the root"""
    return next(find_nodes(root_node, key), None)


def find_nodes_from_here(start_node: AbstractNode, key: Hashable) -> Generator[AbstractNode, None, None]:
    """preorder iterate through all the nodes in the tree with the given key,
    starting with the subtree rooted at the start node,
    then continuing with the parent's subtree, and so on until the total tree.
    Ensure that subtrees are walked only once.

    This is useful if there's reason to believe that
    often enough the nodes that are searched for are close to the start node"""
    return find_nodes_from_here_by_rule(start_node, lambda n_: n_.key == key)


def find_first_node_from_here(start_node: AbstractNode, key: Hashable) -> AbstractNode | None:
    """find the first node matching the tree,
    using the progressive subtree walking from the find_nodes_from_here iterator.

    Use it if the target node should probably be close to the starting one."""
    return next(find_nodes_from_here(start_node, key), None)


def find_nodes_by_rule(root_node: AbstractNode, select: Callable[[AbstractNode], bool]) \
        -> Generator[AbstractNode, None, None]:
    """iterate through the nodes that match the select rule
    (a.k.a. select(node) == True"""
    return filtered_preorder_iterator(root_node, select=select)


def find_first_node_by_rule(root_node: AbstractNode, select: Callable[[AbstractNode], bool]) \
        -> AbstractNode | None:
    """find the first (in preorder) node that matches the select rule
    (a.k.a. select(node) == True"""
    return next(find_nodes_by_rule(root_node, select), None)


def find_nodes_from_here_by_rule(start_node: AbstractNode, select: Callable[[AbstractNode], bool]) \
        -> Generator[AbstractNode, None, None]:
    """iterate through the nodes matching the select rule,
    using the progressive subtree walking"""
    yield from find_nodes_by_rule(start_node, select)
    prev_ = start_node
    node_ = start_node.parent
    while node_ is not None:
        if select(node_):
            yield node_
        for child_ in node_.children:
            if child_ is not prev_:
                yield from find_nodes_by_rule(child_, select)
        prev_ = node_
        node_ = node_.parent


def find_first_node_from_here_by_rule(start_node: AbstractNode,
        select: Callable[[AbstractNode], bool]) -> AbstractNode | None:
    """find the first (in preorder) node that matches the select rule
    (a.k.a. select(node) == True
    using the progressive subtree walking"""
    return next(find_nodes_from_here_by_rule(start_node, select), None)
