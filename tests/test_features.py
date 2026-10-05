from simpletree3 import *


def _build():
    #        0
    #      /   \
    #     1     2
    #    / \     \
    #   3   4     5
    #  /
    # 6
    root = SimpleNode(0)
    n1 = SimpleNode(1, parent=root)
    n2 = SimpleNode(2, parent=root)
    n3 = SimpleNode(3, parent=n1)
    n4 = SimpleNode(4, parent=n1)
    n5 = SimpleNode(5, parent=n2)
    n6 = SimpleNode(6, parent=n3)
    return root, {n.key: n for n in (root, n1, n2, n3, n4, n5, n6)}


class TestNodeFeatures:
    def test_repr(self):
        root, _ = _build()
        assert repr(root) == "SimpleNode(key=0, children=2)"
        assert repr(FlexibleNode("x")) == "FlexibleNode(key='x', children=0)"

    def test_root(self):
        root, n = _build()
        assert n[6].root is root
        assert root.root is root

    def test_path_and_key_path(self):
        root, n = _build()
        assert n[6].path == (root, n[1], n[3], n[6])
        assert n[6].key_path == (0, 1, 3, 6)
        assert root.path == (root,)

    def test_get_descendant(self):
        root, n = _build()
        assert root.get_descendant(1, 3, 6) is n[6]
        assert root.get_descendant() is root
        assert root.get_descendant(1, 99) is None
        assert root.get_descendant(*n[6].key_path[1:]) is n[6]

    def test_ancestor_descendant(self):
        root, n = _build()
        assert root.is_ancestor_of(n[6])
        assert n[1].is_ancestor_of(n[6])
        assert not n[2].is_ancestor_of(n[6])
        assert not n[6].is_ancestor_of(n[6])
        assert n[6].is_descendant_of(root)
        assert not root.is_descendant_of(n[6])

    def test_detach(self):
        root, n = _build()
        n[1].detach()
        assert n[1].is_root
        assert not root.has_child(1)
        assert n[6].root is n[1]
        n[1].detach()  # already a root: no-op
        assert n[1].is_root

    def test_size(self):
        root, n = _build()
        assert root.size == 7
        assert n[1].size == 4
        assert n[6].size == 1
        assert count_nodes(n[2]) == 2


class TestLowestCommonAncestor:
    def test_lca(self):
        root, n = _build()
        assert lowest_common_ancestor(n[6], n[4]) is n[1]
        assert lowest_common_ancestor(n[6], n[5]) is root
        assert lowest_common_ancestor(n[3], n[6]) is n[3]
        assert lowest_common_ancestor(n[6], n[6]) is n[6]

    def test_lca_different_trees(self):
        _, n = _build()
        assert lowest_common_ancestor(n[6], SimpleNode(0)) is None
