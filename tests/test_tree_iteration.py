import unittest

from simpletree3 import *


def build_simple_tree():
    nodes_ = dict()
    root_ = SimpleNode(key=0)
    nodes_[0] = root_
    for n_ in range(1, 16):
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


_preorder_list = [0, 1, 3, 9, 10, 11, 4, 12, 13, 14, 5, 15, 2, 6, 7, 8]
_postorder_list = [9, 10, 11, 3, 12, 13, 14, 4, 15, 5, 1, 6, 7, 8, 2, 0]
_level_order_list = list(range(16))


class TestTreeIteration(unittest.TestCase):
    def test_preorder_iterator(self):
        root_ = build_simple_tree()
        po_ = list(n.key for n in preorder_iterator(root_))
        self.assertListEqual(po_, _preorder_list, "preorder iterator result did not match")
        root_ = build_flex_tree()
        po_ = list(n.key for n in preorder_iterator(root_))
        self.assertListEqual(po_, _preorder_list, "preorder iterator result did not match")

    def test_filtered_preorder_iterator(self):
        root_ = build_simple_tree()
        po_ = list(n.key for n in filtered_preorder_iterator(root_, select=lambda x: x.key % 2))
        self.assertListEqual(po_, [k for k in _preorder_list if k % 2],
            "filtered preorder iterator result did not match (select)")

        po_ = list(n.key for n in filtered_preorder_iterator(root_, ignore=lambda x: x.key == 2))
        self.assertListEqual(po_, _preorder_list[:-4],
            "filtered preorder iterator result did not match (ignore)")

        root_ = build_flex_tree()
        po_ = list(n.key for n in filtered_preorder_iterator(root_, select=lambda x: x.key % 2))
        self.assertListEqual(po_, [k for k in _preorder_list if k % 2],
            "filtered preorder iterator result did not match (select)")

        po_ = list(n.key for n in filtered_preorder_iterator(root_, ignore=lambda x: x.key == 2))
        self.assertListEqual(po_, _preorder_list[:-4],
            "filtered preorder iterator result did not match (ignore)")

    def test_postorder_iterator(self):
        root_ = build_simple_tree()
        po_ = list(n.key for n in postorder_iterator(root_))
        self.assertListEqual(po_, _postorder_list, "postorder iterator result did not match")

        root_ = build_flex_tree()
        po_ = list(n.key for n in postorder_iterator(root_))
        self.assertListEqual(po_, _postorder_list, "postorder iterator result did not match")

    def test_filtered_postorder_iterator(self):
        root_ = build_simple_tree()
        po_ = list(n.key for n in filtered_postorder_iterator(root_, select=lambda x: x.key % 2))
        self.assertListEqual(po_, [k for k in _postorder_list if k % 2],
            "filtered postorder iterator result did not match (select)")

        po_ = list(n.key for n in filtered_postorder_iterator(root_, ignore=lambda x: x.key == 2))
        self.assertListEqual(po_, _postorder_list[:-5] + [0],
            "filtered postorder iterator result did not match (ignore)")

        root_ = build_flex_tree()
        po_ = list(n.key for n in filtered_postorder_iterator(root_, select=lambda x: x.key % 2))
        self.assertListEqual(po_, [k for k in _postorder_list if k % 2],
            "filtered postorder iterator result did not match (select)")

        po_ = list(n.key for n in filtered_postorder_iterator(root_, ignore=lambda x: x.key == 2))
        self.assertListEqual(po_, _postorder_list[:-5] + [0],
            "filtered postorder iterator result did not match (ignore)")

    def test_level_order_iterator(self):
        root_ = build_simple_tree()
        po_ = list(n.key for n in level_order_iterator(root_))
        self.assertListEqual(po_, _level_order_list, "simple level order iterator result did not match")

        root_ = build_flex_tree()
        po_ = list(n.key for n in level_order_iterator(root_))
        self.assertListEqual(po_, _level_order_list, "flex level order iterator result did not match")

    def test_filtered_level_order_iterator(self):
        root_ = build_simple_tree()
        # print("all nodes: ",
        #     [(n.key, n.depth) for n in level_order_iterator(root_)])
        po_ = list(n.key for n in filtered_level_order_iterator(root_,
                select=lambda x: x.key % 2))
        self.assertListEqual(po_, [k for k in _level_order_list if k % 2],
            "simple filtered level order iterator result did not match (select)")

        po_ = list(n.key for n in filtered_level_order_iterator(root_, ignore=lambda x: x.key == 2))
        ans_ = [0, 1, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15]
        self.assertListEqual(po_, ans_,
            "simple filtered level order iterator result did not match (ignore)")

        po_ = list(n.key for n in filtered_level_order_iterator(root_, ignore=lambda x: x.key == 0))
        self.assertListEqual(po_, [],
            "simple filtered level order iterator result did not match (ignore all)")

        root_ = build_flex_tree()
        po_ = list(n.key for n in filtered_level_order_iterator(root_, select=lambda x: x.key % 2))
        self.assertListEqual(po_, [k for k in _level_order_list if k % 2],
            "flex filtered level order iterator result did not match (select)")

        po_ = list(n.key for n in filtered_level_order_iterator(root_, ignore=lambda x: x.key == 2))
        self.assertListEqual(po_, ans_,
            "flex filtered level order iterator result did not match (ignore)")

        po_ = list(n.key for n in filtered_level_order_iterator(root_, ignore=lambda x: x.key == 0))
        self.assertListEqual(po_, [],
            "flex filtered level order iterator result did not match (ignore all)")

    def test_leaves_iterator(self):
        root_ = build_simple_tree()
        lil_ = list(n.key for n in leaves_iterator(root_))
        leaves_ = [9, 10, 11, 12, 13, 14, 15, 6, 7, 8]
        self.assertListEqual(lil_, leaves_, "leaves iterator result did not match")

        root_ = build_flex_tree()
        lil_ = list(n.key for n in leaves_iterator(root_))
        self.assertListEqual(lil_, leaves_, "leaves iterator result did not match")

    def test_filtered_leaves_iterator(self):
        root_ = build_simple_tree()

        def _select(x):
            return x.key % 5

        def _ignore(x):
            return x.key == 3

        lil_ = list(n.key for n in filtered_leaves_iterator(root_, _select, _ignore))
        leaves_ = [12, 13, 14, 6, 7, 8]
        self.assertListEqual(lil_, leaves_, "leaves iterator result did not match")

        root_ = build_flex_tree()
        lil_ = list(n.key for n in filtered_leaves_iterator(root_, _select, _ignore))
        self.assertListEqual(lil_, leaves_, "leaves iterator result did not match")
