import random

import pytest

from simpletree3 import *


# reference recursive implementations, used to check that the iterative walks
# visit the nodes in exactly the same order

def _ref_preorder(node, select=None, ignore=None):
    if ignore and ignore(node):
        return
    if select is None or select(node):
        yield node
    for c in node.children:
        yield from _ref_preorder(c, select, ignore)


def _ref_postorder(node, select=None, ignore=None):
    if ignore and ignore(node):
        return
    for c in node.children:
        yield from _ref_postorder(c, select, ignore)
    if select is None or select(node):
        yield node


def _ref_level_order(node, select=None, ignore=None):
    level = [] if ignore and ignore(node) else [node]
    while level:
        for n in level:
            if select is None or select(n):
                yield n
        level = [c for n in level for c in n.children if not (ignore and ignore(c))]


def _ref_leaves(node, select=None, ignore=None):
    for n in _ref_preorder(node, ignore=ignore):
        if n.is_leaf and (select is None or select(n)):
            yield n


def _random_tree(n_nodes=300, seed=1234):
    rng = random.Random(seed)
    nodes = [SimpleNode(0)]
    for k in range(1, n_nodes):
        nodes.append(SimpleNode(k, parent=rng.choice(nodes)))
    return nodes[0]


def _keys(it):
    return [n.key for n in it]


class TestIterativeWalksMatchRecursive:
    root = _random_tree()
    select = staticmethod(lambda n: n.key % 3 == 0)
    ignore = staticmethod(lambda n: n.key % 7 == 1)

    @pytest.mark.parametrize("fn, ref", [
        (preorder_iterator, _ref_preorder),
        (postorder_iterator, _ref_postorder),
        (level_order_iterator, _ref_level_order),
        (leaves_iterator, _ref_leaves),
    ])
    def test_plain(self, fn, ref):
        assert _keys(fn(self.root)) == _keys(ref(self.root))

    @pytest.mark.parametrize("fn, ref", [
        (filtered_preorder_iterator, _ref_preorder),
        (filtered_postorder_iterator, _ref_postorder),
        (filtered_level_order_iterator, _ref_level_order),
        (filtered_leaves_iterator, _ref_leaves),
    ])
    @pytest.mark.parametrize("use_select, use_ignore", [
        (False, False), (True, False), (False, True), (True, True)])
    def test_filtered(self, fn, ref, use_select, use_ignore):
        sel = self.select if use_select else None
        ign = self.ignore if use_ignore else None
        assert _keys(fn(self.root, sel, ign)) == _keys(ref(self.root, sel, ign))

    def test_ignored_root(self):
        for fn in (filtered_preorder_iterator, filtered_postorder_iterator,
                   filtered_level_order_iterator, filtered_leaves_iterator):
            assert list(fn(self.root, ignore=lambda n: True)) == []


class TestDeepTrees:
    DEPTH = 10_000

    def _chain(self):
        root = node = SimpleNode(0)
        for i in range(1, self.DEPTH):
            node = SimpleNode(i, parent=node)
        return root, node

    def test_walks_do_not_hit_recursion_limit(self):
        root, leaf = self._chain()
        assert sum(1 for _ in preorder_iterator(root)) == self.DEPTH
        assert sum(1 for _ in postorder_iterator(root)) == self.DEPTH
        assert sum(1 for _ in level_order_iterator(root)) == self.DEPTH
        assert list(leaves_iterator(root)) == [leaf]
        assert find_first_node(root, self.DEPTH - 1) is leaf
        assert find_first_node_from_here(leaf, 0) is root
        assert root.height == self.DEPTH - 1
        assert leaf.depth == self.DEPTH - 1

    def test_recursive_remove_children(self):
        root, leaf = self._chain()
        root.remove_children(recursive=True)
        assert root.is_leaf
        assert leaf.parent is None


class TestFindIsNotCached:
    def test_find_first_node_sees_new_nodes(self):
        root = SimpleNode(0)
        assert find_first_node(root, 5) is None
        n5 = SimpleNode(5, parent=root)
        assert find_first_node(root, 5) is n5

    def test_find_first_node_forgets_removed_nodes(self):
        root = SimpleNode(0)
        SimpleNode(5, parent=root)
        assert find_first_node(root, 5) is not None
        root.remove_child(5)
        assert find_first_node(root, 5) is None

    def test_all_first_finders(self):
        root = SimpleNode(0)
        start = SimpleNode(1, parent=root)
        rule = lambda n: n.key == 9
        assert find_first_node_from_here(start, 9) is None
        assert find_first_node_by_rule(root, rule) is None
        assert find_first_node_from_here_by_rule(start, rule) is None
        n9 = SimpleNode(9, parent=root)
        assert find_first_node_from_here(start, 9) is n9
        assert find_first_node_by_rule(root, rule) is n9
        assert find_first_node_from_here_by_rule(start, rule) is n9


class TestTreeConsistency:
    @pytest.mark.parametrize("cls", [SimpleNode, FlexibleNode])
    def test_del_parent_removes_from_children(self, cls):
        root = cls(0)
        child = cls(1, parent=root)
        del child.parent
        assert child.parent is None
        assert not root.has_child(1)
        assert root.children_count == 0

    @pytest.mark.parametrize("cls", [SimpleNode, FlexibleNode])
    def test_failed_reparent_duplicate_leaves_tree_unchanged(self, cls):
        a = cls("a")
        b = cls("b", parent=a)
        x = cls("x", parent=b)
        other = cls("o")
        cls("x", parent=other)
        with pytest.raises(DuplicateChildNode):
            x.parent = other
        assert x.parent is b
        assert b.child("x") is x

    @pytest.mark.parametrize("cls", [SimpleNode, FlexibleNode])
    def test_failed_reparent_cycle_leaves_tree_unchanged(self, cls):
        a = cls("a")
        b = cls("b", parent=a)
        c = cls("c", parent=b)
        with pytest.raises(InvalidNodeOperation):
            b.parent = c
        assert b.parent is a
        assert a.child("b") is b

    def test_reparent_moves_node(self):
        a = SimpleNode("a")
        b = SimpleNode("b", parent=a)
        c = SimpleNode("c", parent=a)
        x = SimpleNode("x", parent=b)
        x.parent = c
        assert not b.has_child("x")
        assert c.child("x") is x

    def test_add_child_already_present_is_noop(self):
        a = SimpleNode("a")
        b = SimpleNode("b", parent=a)
        a.add_child(b)
        assert a.children_count == 1

    def test_duplicate_child_exposes_key(self):
        a = SimpleNode("a")
        SimpleNode("b", parent=a)
        with pytest.raises(DuplicateChildNode) as exc:
            a.add_child(SimpleNode("b"))
        assert exc.value.key == "b"

    def test_kwargs_cannot_overwrite_internals(self):
        root = SimpleNode(0)
        with pytest.raises(InvalidNodeOperation):
            SimpleNode(1, parent=root, _SimpleNode__parent=None)
        assert root.children_count == 0
        assert SimpleNode(2, payload="x").payload == "x"  # type: ignore[attr-defined]


class SizedNode(SimpleNode):
    """a node whose truthiness depends on its children count"""
    def __len__(self):
        return self.children_count


class EqNode(SimpleNode):
    """a node where all nodes compare equal"""
    def __eq__(self, other):
        return True

    __hash__ = SimpleNode.__hash__


class TestNodesWithCustomDunders:
    def test_falsy_leaf_parent_is_attached(self):
        p = SizedNode(0)
        q = SizedNode(1, parent=p)
        z = SizedNode(2, parent=q)
        assert q.parent is p
        assert z.depth == 2
        assert p.height == 2
        assert list(reverse_path_iterator(z)) == [z, q, p]
        assert find_first_node_from_here(z, 0) is p
        assert z.ancestors == (p, q)
        assert z.siblings_count == 0

    def test_eq_does_not_confuse_identity(self):
        a = EqNode("a")
        b = EqNode("b", parent=a)
        c = EqNode("c")
        c.parent = a
        assert a.children_count == 2
        assert [n.key for n in b.siblings] == ["c"]


class HookNode(FlexibleNode):
    def __init__(self, key, parent=None):
        self.events = []
        super().__init__(key, parent)

    def _pre_assign_parent_hook(self, other):
        self.events.append(("pre_assign", None if other is None else other.key))

    def _post_assign_parent_hook(self, other):
        self.events.append(("post_assign", None if other is None else other.key))

    def _pre_delete_parent_hook(self):
        self.events.append(("pre_delete",))

    def _post_delete_parent_hook(self):
        self.events.append(("post_delete",))


class TestFlexibleHooks:
    DELETE = [("pre_delete",), ("post_delete",)]

    def test_remove_child_fires_delete_hooks(self):
        root = HookNode(0)
        child = HookNode(1, parent=root)
        child.events.clear()
        assert root.remove_child(1) is child
        assert child.events == self.DELETE

    def test_remove_children_fires_delete_hooks(self):
        root = HookNode(0)
        kids = [HookNode(k, parent=root) for k in range(1, 4)]
        grandkid = HookNode(9, parent=kids[0])
        for n in kids + [grandkid]:
            n.events.clear()
        root.remove_children(recursive=True)
        for n in kids + [grandkid]:
            assert n.events == self.DELETE

    def test_detach_fires_delete_hooks(self):
        root = HookNode(0)
        child = HookNode(1, parent=root)
        child.events.clear()
        child.detach()
        assert child.events == self.DELETE
        assert root.children_count == 0


class MixedKeyNode(SimpleNode):
    sort_children = False


class TestChildrenOrdering:
    def test_mixed_keys_with_insertion_order(self):
        root = MixedKeyNode(0)
        for k in (3, "a", 1, ("t", 2)):
            MixedKeyNode(k, parent=root)
        assert [n.key for n in root.children] == [3, "a", 1, ("t", 2)]
        assert [n.key for n in preorder_iterator(root)] == [0, 3, "a", 1, ("t", 2)]

    def test_default_is_sorted(self):
        root = SimpleNode(0)
        for k in (3, 1, 2):
            SimpleNode(k, parent=root)
        assert [n.key for n in root.children] == [1, 2, 3]

    def test_children_can_be_mutated_while_iterating(self):
        for cls in (SimpleNode, MixedKeyNode):
            root = cls(0)
            for k in range(5):
                cls(k + 1, parent=root)
            for c in root.children:
                c.detach()
            assert root.children_count == 0


class TestNoOps:
    def test_same_parent_assignment_is_noop(self):
        root = HookNode(0)
        child = HookNode(1, parent=root)
        child.parent = root
        assert root.children_count == 1 and child.parent is root

    def test_remove_children_of_leaf(self):
        leaf = SimpleNode(0)
        assert leaf.remove_children() is None
        assert leaf.remove_children(recursive=True) is None
