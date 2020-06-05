import unittest

from simpletree3 import *


_max_key = 16


def build_simple_tree():
    nodes_ = dict()
    root_ = SimpleNode(key=0)
    nodes_[0] = root_
    for n_ in range(1, _max_key):
        node_ = SimpleNode(key=n_, parent=nodes_[n_ // 3])
        nodes_[n_] = node_
    return root_


def build_flex_tree():
    nodes_ = dict()
    root_ = FlexibleNode(key=0)
    nodes_[0] = root_
    for n_ in range(1, 16):
        node_ = FlexibleNode(key=n_, parent=nodes_[n_ // 3])
        nodes_[n_] = node_
    return root_


class TestTreeSearch(unittest.TestCase):
    def test_find_first(self):
        tree_ = build_simple_tree()
        node_ = find_first_node(tree_, key=5)
        self.assertEqual(node_.key, 5)

        tree_ = build_flex_tree()
        node_ = find_first_node(tree_, key=5)
        self.assertEqual(node_.key, 5)

        node_ = find_first_node(tree_, key=50)
        self.assertEqual(node_, None)

    def test_find_list(self):
        tree_ = build_simple_tree()
        nodes_ = list(find_nodes(tree_, key=5))
        self.assertListEqual([node_.key for node_ in nodes_], [5])

        tree_ = build_flex_tree()
        nodes_ = list(find_nodes(tree_, key=5))
        self.assertListEqual([node_.key for node_ in nodes_], [5])

        nodes_ = list(find_nodes(tree_, key=50))
        self.assertEqual(len(nodes_), 0)

    def test_find_first_rule(self):
        tree_ = build_simple_tree()
        node_ = find_first_node_by_rule(tree_, select=lambda x: 4 < x.key < 6)
        self.assertEqual(node_.key, 5)

        tree_ = build_flex_tree()
        node_ = find_first_node_by_rule(tree_, select=lambda x: 4 < x.key < 6)
        self.assertEqual(node_.key, 5)

        node_ = find_first_node_by_rule(tree_, select=lambda x: 45 < x.key)
        self.assertEqual(node_, None)

    def test_find_list_rule(self):
        tree_ = build_simple_tree()
        nodes_ = list(find_nodes_by_rule(tree_, select=lambda x: x.key > 4))
        self.assertListEqual(sorted(node_.key for node_ in nodes_), list(range(5, _max_key)))

        tree_ = build_flex_tree()
        nodes_ = list(find_nodes_by_rule(tree_, select=lambda x: x.key > 4))
        self.assertListEqual(sorted(node_.key for node_ in nodes_), list(range(5, _max_key)))

        nodes_ = list(find_nodes_by_rule(tree_, select=lambda x: x.key > 45))
        self.assertEqual(len(nodes_), 0)

    def test_find_first_hinted(self):
        tree_ = build_simple_tree()
        node_ = find_first_node(tree_, key=5)
        node_ = find_first_node_from_here(node_, key=9)
        self.assertEqual(node_.key, 9)
        node_ = find_first_node_from_here(node_, key=0)
        self.assertEqual(node_.key, 0)
        node_ = find_first_node_from_here(node_, key=100)
        self.assertEqual(node_, None)

        tree_ = build_flex_tree()
        node_ = find_first_node(tree_, key=5)
        node_ = find_first_node_from_here(node_, key=9)
        self.assertEqual(node_.key, 9)
        node_ = find_first_node_from_here(node_, key=0)
        self.assertEqual(node_.key, 0)
        node_ = find_first_node_from_here(node_, key=100)
        self.assertEqual(node_, None)

    def test_find_list_hinted(self):
        tree_ = build_simple_tree()
        node_ = find_first_node(tree_, key=9)
        nodes_ = list(find_nodes_from_here(node_, key=5))
        self.assertListEqual([node_.key for node_ in nodes_], [5])

        tree_ = build_flex_tree()
        node_ = find_first_node(tree_, key=9)
        nodes_ = list(find_nodes_from_here(node_, key=5))
        self.assertListEqual([node_.key for node_ in nodes_], [5])
        nodes_ = list(find_nodes_from_here(node_, key=50))
        self.assertEqual(len(nodes_), 0)

    def test_find_first_hinted_rule(self):
        tree_ = build_simple_tree()
        node_ = find_first_node(tree_, key=5)
        node_ = find_first_node_from_here_by_rule(node_, select=lambda x: x.key == 9)
        self.assertEqual(node_.key, 9)
        node_ = find_first_node_from_here_by_rule(node_, select=lambda x: 0 == x.key % 99)
        self.assertEqual(node_.key, 0)
        node_ = find_first_node_from_here_by_rule(node_, select=lambda x: x.key >= 99)
        self.assertEqual(node_, None)

        tree_ = build_flex_tree()
        node_ = find_first_node(tree_, key=5)
        node_ = find_first_node_from_here_by_rule(node_, select=lambda x: x.key == 9)
        self.assertEqual(node_.key, 9)
        node_ = find_first_node_from_here_by_rule(node_, select=lambda x: x.key >= 99)
        self.assertEqual(node_, None)

    def test_find_list_hinted_rule(self):
        tree_ = build_simple_tree()
        node_ = find_first_node(tree_, key=9)
        nodes_ = list(find_nodes_from_here_by_rule(node_, select=lambda x: x.key == 5))
        self.assertListEqual([node_.key for node_ in nodes_], [5])
        nodes_ = list(find_nodes_from_here_by_rule(node_, select=lambda x: x.key >= 100))
        self.assertEqual(len(nodes_), 0)

        tree_ = build_flex_tree()
        node_ = find_first_node(tree_, key=9)
        nodes_ = list(find_nodes_from_here_by_rule(node_, select=lambda x: x.key == 5))
        self.assertListEqual([node_.key for node_ in nodes_], [5])
        nodes_ = list(find_nodes_from_here_by_rule(node_, select=lambda x: x.key >= 100))
        self.assertEqual(len(nodes_), 0)
