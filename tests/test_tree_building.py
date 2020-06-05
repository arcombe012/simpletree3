import unittest

from simpletree3 import *

KEYS = list(range(20))


def _parent_from_key(key: int):
    if key:
        return key // 3
    return None


class TestTreeBuilding(unittest.TestCase):
    def test_build_simple_tree_int(self):
        nodes_ = dict()
        for key in KEYS:
            if key > 0:
                parent_node_ = nodes_[_parent_from_key(key)]
                nodes_[key] = SimpleNode(key=key, parent=parent_node_)
            else:
                nodes_[0] = SimpleNode(key=0)

        self.assertEqual(len(KEYS), len(nodes_), "not all nodes were inserted")

    def test_build_simple_tree_int_2(self):
        nodes_ = dict()
        for key in KEYS:
            if key > 0:
                parent_node_ = nodes_[_parent_from_key(key)]
                nodes_[key] = SimpleNode(key=key)
                parent_node_.add_child(nodes_[key])
            else:
                nodes_[0] = SimpleNode(key=0)

        self.assertEqual(len(KEYS), len(nodes_), "not all nodes were inserted")

    def test_build_flexible_tree_int(self):
        nodes_ = dict()
        for key in KEYS:
            if key > 0:
                parent_node_ = nodes_[_parent_from_key(key)]
                nodes_[key] = FlexibleNode(key=key, parent=parent_node_)
            else:
                nodes_[0] = FlexibleNode(key=0)

        self.assertEqual(len(KEYS), len(nodes_), "not all nodes were inserted")

    def test_build_flexible_tree_int_2(self):
        nodes_ = dict()
        for key in KEYS:
            if key > 0:
                parent_node_ = nodes_[_parent_from_key(key)]
                nodes_[key] = FlexibleNode(key=key)
                parent_node_.add_child(nodes_[key])
            else:
                nodes_[0] = FlexibleNode(key=0)

        self.assertEqual(len(KEYS), len(nodes_), "not all nodes were inserted")

    def test_build_simple_tree_str(self):
        nodes_ = dict()
        for key in KEYS:
            skey = str(key)
            if key > 0:
                parent_node_ = nodes_[str(_parent_from_key(key))]
                nodes_[skey] = SimpleNode(key=skey, parent=parent_node_)
            else:
                nodes_[skey] = SimpleNode(key=skey)

        self.assertEqual(len(KEYS), len(nodes_), "not all nodes were inserted")

    def test_build_flexible_tree_str(self):
        nodes_ = dict()
        for key in KEYS:
            skey = str(key)
            if key > 0:
                parent_node_ = nodes_[str(_parent_from_key(key))]
                nodes_[skey] = FlexibleNode(key=skey, parent=parent_node_)
            else:
                nodes_[skey] = FlexibleNode(key=skey)

        self.assertEqual(len(KEYS), len(nodes_), "not all nodes were inserted")

    def test_bad_build_simple_tree_1(self):
        with self.assertRaises(DuplicateChildNode):
            root_ = SimpleNode(key=0)
            nn = 5
            [SimpleNode(key=k, parent=root_) for k in range(1, nn + 1)]
            self.assertEqual(nn, root_.children_count, "invalid number of children")
            SimpleNode(key=2, parent=root_)

    def test_bad_build_simple_tree_2(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = SimpleNode(key=0)
            nn = 5
            [SimpleNode(key=k, parent=root_) for k in range(1, nn + 1)]
            root_.parent = root_.child(1)

    def test_bad_build_simple_tree_3(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = SimpleNode(key=0)
            nn = 5
            [SimpleNode(key=k, parent=root_) for k in range(1, nn + 1)]
            root_.parent = root_

    def test_bad_build_simple_tree_4(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = SimpleNode(key=0)
            nn = 5
            [SimpleNode(key=k, parent=root_) for k in range(1, nn + 1)]
            root_.add_child(root_)

    def test_bad_build_flexible_tree_1(self):
        with self.assertRaises(DuplicateChildNode):
            root_ = FlexibleNode(key=0)
            nn = 5
            [FlexibleNode(key=k, parent=root_) for k in range(1, nn + 1)]
            self.assertEqual(nn, root_.children_count, "invalid number of children")
            SimpleNode(key=2, parent=root_)

    def test_bad_build_flexible_tree_2(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = FlexibleNode(key=0)
            nn = 5
            [FlexibleNode(key=k, parent=root_) for k in range(1, nn + 1)]
            root_.parent = root_.child(1)

    def test_bad_build_flexible_tree_3(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = FlexibleNode(key=0)
            nn = 5
            [FlexibleNode(key=k, parent=root_) for k in range(1, nn+1)]
            root_.parent = root_

    def test_bad_build_flexible_tree_4(self):
        with self.assertRaises(InvalidNodeOperation):
            root_ = FlexibleNode(key=0)
            nn = 5
            [FlexibleNode(key=k, parent=root_) for k in range(1, nn+1)]
            root_.add_child(root_)

    def test_simple_delete_parent(self):
        root_ = SimpleNode(key=0)
        n1_ = SimpleNode(key=1, parent=root_)
        n2_ = SimpleNode(key=2, parent=root_)
        del n2_.parent
        del n1_.parent

    def test_flexible_delete_parent(self):
        root_ = FlexibleNode(key=0)
        n1_ = FlexibleNode(key=1, parent=root_)
        n2_ = FlexibleNode(key=2, parent=root_)
        del n2_.parent
        del n1_.parent

    def test_simple_delete_child(self):
        root_ = SimpleNode(key=0)
        n1_ = SimpleNode(key=1, parent=root_)
        n2_ = SimpleNode(key=2, parent=root_)
        n3_ = SimpleNode(key=3, parent=n1_)
        n4_ = SimpleNode(key=4, parent=n1_)
        n5_ = SimpleNode(key=5, parent=n3_)
        n6_ = SimpleNode(key=6, parent=n2_)
        n7_ = SimpleNode(key=7, parent=n2_)
        n8_ = SimpleNode(key=8, parent=n2_)

        self.assertEqual(n2_.children_count, 3)
        n2_.remove_child(key=None)
        n2_.remove_child(key=99)
        self.assertEqual(n2_.children_count, 3)
        n2_.remove_child(key=6)
        self.assertEqual(n2_.children_count, 2)
        n2_.remove_children()
        self.assertEqual(n2_.children_count, 0)
        n1_.remove_child(key=3, recursive=True)
        self.assertEqual(n5_.parent, None)
        self.assertEqual(n1_.children_count, 1)

    def test_flexible_delete_child(self):
        root_ = FlexibleNode(key=0)
        n1_ = FlexibleNode(key=1, parent=root_)
        n2_ = FlexibleNode(key=2, parent=root_)
        n3_ = FlexibleNode(key=3, parent=n1_)
        n4_ = FlexibleNode(key=4, parent=n1_)
        n5_ = FlexibleNode(key=5, parent=n3_)
        n6_ = FlexibleNode(key=6, parent=n2_)
        n7_ = FlexibleNode(key=7, parent=n2_)
        n8_ = FlexibleNode(key=8, parent=n2_)

        self.assertEqual(n2_.children_count, 3)
        n2_.remove_child(key=None)
        n2_.remove_child(key=99)
        self.assertEqual(n2_.children_count, 3)
        n2_.remove_child(key=6)
        self.assertEqual(n2_.children_count, 2)
        n2_.remove_children()
        self.assertEqual(n2_.children_count, 0)
        n1_.remove_child(key=3, recursive=True)
        self.assertEqual(n5_.parent, None)
        self.assertEqual(n1_.children_count, 1)
