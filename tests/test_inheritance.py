import unittest

from simpletree3 import *


class MyNode(FlexibleNode):
    def __init__(self, key, parent=None):
        self.info_pre = None
        self.info_post = None
        super().__init__(key, parent)

    def _pre_assign_parent_hook(self, other):
        self.info_pre = (self.key, other.key)

    def _post_assign_parent_hook(self, other):
        self.info_post = (self.key, other.key)

    def _pre_delete_parent_hook(self):
        self.info_pre = (self.key, None)

    def _post_delete_parent_hook(self):
        self.info_post = (self.key, None)


class TestInheritance(unittest.TestCase):
    def test_inheritance(self):
        root_ = MyNode(0)
        node_ = root_
        for i in range(1, 10):
            node_ = MyNode(key=i, parent=find_first_node_from_here(node_, i // 3))

        for n_ in preorder_iterator(root_):
            if n_.is_root:
                continue
            t_ = (n_.key, n_.parent.key)
            self.assertEqual(n_.info_pre, t_, "pre assign parent hook was not called")
            self.assertEqual(n_.info_post, t_, "post assign parent hook was not called")

        del node_.parent
        t_ = (node_.key, None)
        self.assertEqual(node_.info_pre, t_, "pre delete parent hook was not called")
        self.assertEqual(node_.info_post, t_, "post delete parent hook was not called")
