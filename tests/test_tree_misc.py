import unittest

from simpletree3 import *


class TestTreeMisc(unittest.TestCase):
    def test_set_key(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = SimpleNode(key=0)
            root_.key = 1

    def test_del_key(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = SimpleNode(key=0)
            del root_.key

    def test_set_key_flex(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = FlexibleNode(key=0)
            root_.key = 1

    def test_del_key_flex(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = FlexibleNode(key=0)
            del root_.key

    def test_set_parent_error(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = SimpleNode(key=0)
            root_.parent = root_

    def test_set_parent_error_flex(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = FlexibleNode(key=0)
            root_.parent = root_

    def test_has_child(self):
        root_ = SimpleNode(key=0)
        root_.add_child(SimpleNode(key=1, parent=None))
        root_.add_child(SimpleNode(key=2, parent=root_))
        self.assertEqual(root_.has_child(1), True)
        self.assertEqual(root_.has_child(-1), False)

    def test_has_child_flex(self):
        root_ = FlexibleNode(key=0)
        root_.add_child(FlexibleNode(key=1, parent=None))
        root_.add_child(FlexibleNode(key=2, parent=root_))
        self.assertEqual(root_.has_child(1), True)
        self.assertEqual(root_.has_child(-1), False)

    def test_list_siblings(self):
        root_ = SimpleNode(key=0)
        for i in range(5):
            root_.add_child(SimpleNode(key=i))
        n1 = root_.child(1)
        print(root_.children_count)
        for nn in root_.children:
            print(nn, nn.key, nn.parent)
        self.assertEqual(root_.siblings_count, 0, "sibling count did not match for root")
        self.assertEqual(n1.siblings_count, 4, "sibling count did not match")
        self.assertListEqual(list(n.key for n in root_.siblings), [], "root siblings did not match")
        self.assertListEqual(list(n.key for n in n1.siblings), [0, 2, 3, 4], "siblings did not match")

    def test_list_siblings_flex(self):
        root_ = FlexibleNode(key=0)
        for i in range(5):
            root_.add_child(FlexibleNode(key=i))
        n1 = root_.child(1)
        self.assertEqual(root_.siblings_count, 0, "sibling count did not match for root (flex)")
        self.assertEqual(n1.siblings_count, 4, "sibling count did not match (flex)")
        self.assertListEqual(list(n.key for n in root_.siblings), [], "root siblings did not match (flex)")
        self.assertListEqual(list(n.key for n in n1.siblings), [0, 2, 3, 4],
                          "siblings did not match (flex)")

    def test_ancestors(self):
        root_ = SimpleNode(key=0)
        node_ = root_
        for i in range(1, 5):
            node_ = SimpleNode(key=i, parent=node_)
        self.assertListEqual(list(n.key for n in node_.ancestors), list(range(5))[:-1])
        self.assertListEqual(list(root_.ancestors), [])

    def test_ancestors_flex(self):
        root_ = FlexibleNode(key=0)
        node_ = root_
        for i in range(1, 5):
            node_ = FlexibleNode(key=i, parent=node_)
        self.assertListEqual(list(n.key for n in node_.ancestors), list(range(5))[:-1])
        self.assertListEqual(list(root_.ancestors), [])

    def test_root_leaf(self):
        root_ = SimpleNode(key=0)
        node_ = root_
        for i in range(1, 5):
            node_ = SimpleNode(key=i, parent=node_)
        self.assertEqual(root_.is_root, True)
        self.assertEqual(root_.is_leaf, False)
        self.assertEqual(node_.is_root, False)
        self.assertEqual(node_.is_leaf, True)

    def test_root_leaf_flex(self):
        root_ = FlexibleNode(key=0)
        node_ = root_
        for i in range(1, 5):
            node_ = FlexibleNode(key=i, parent=node_)
        self.assertEqual(root_.is_root, True)
        self.assertEqual(root_.is_leaf, False)
        self.assertEqual(node_.is_root, False)
        self.assertEqual(node_.is_leaf, True)

    def test_height_depth(self):
        root_ = SimpleNode(key=0)
        node_ = root_
        for i in range(1, 5):
            node_ = SimpleNode(key=i, parent=node_)
        self.assertEqual(root_.height, 4)
        self.assertEqual(root_.depth, 0)
        self.assertEqual(node_.height, 0)
        self.assertEqual(node_.depth, 4)
        node_ = next(root_.children)
        self.assertEqual(node_.height, 3)
        self.assertEqual(node_.depth, 1)
        n_ = root_.remove_child(node_.key)
        self.assertEqual(root_.height, 0)
        self.assertEqual(root_.depth, 0)
        self.assertEqual(n_.height, 3)
        self.assertEqual(n_.depth, 0)
        root_.add_child(n_)
        self.assertEqual(root_.height, 4)
        self.assertEqual(root_.depth, 0)
        self.assertEqual(n_.height, 3)
        self.assertEqual(n_.depth, 1)
        n_.parent = None
        self.assertEqual(root_.height, 0)
        self.assertEqual(root_.depth, 0)
        self.assertEqual(n_.height, 3)
        self.assertEqual(n_.depth, 0)
        n_.parent = root_
        self.assertEqual(root_.height, 4)
        self.assertEqual(root_.depth, 0)
        self.assertEqual(n_.height, 3)
        self.assertEqual(n_.depth, 1)


    def test_height_depth_flex(self):
        root_ = FlexibleNode(key=0)
        node_ = root_
        for i in range(1, 5):
            node_ = FlexibleNode(key=i, parent=node_)
        self.assertEqual(root_.height, 4)
        self.assertEqual(root_.depth, 0)
        self.assertEqual(node_.height, 0)
        self.assertEqual(node_.depth, 4)
        node_ = next(root_.children)
        self.assertEqual(node_.height, 3)
        self.assertEqual(node_.depth, 1)
        n_ = root_.remove_child(node_.key)
        self.assertEqual(root_.height, 0)
        self.assertEqual(root_.depth, 0)
        self.assertEqual(n_.height, 3)
        self.assertEqual(n_.depth, 0)
        root_.add_child(n_)
        self.assertEqual(root_.height, 4)
        self.assertEqual(root_.depth, 0)
        self.assertEqual(n_.height, 3)
        self.assertEqual(n_.depth, 1)
        n_.parent = None
        self.assertEqual(root_.height, 0)
        self.assertEqual(root_.depth, 0)
        self.assertEqual(n_.height, 3)
        self.assertEqual(n_.depth, 0)
        n_.parent = root_
        self.assertEqual(root_.height, 4)
        self.assertEqual(root_.depth, 0)
        self.assertEqual(n_.height, 3)
        self.assertEqual(n_.depth, 1)
