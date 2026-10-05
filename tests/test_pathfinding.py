import pytest

from simpletree3 import *

# Helper function to build a consistent test tree
def build_sample_tree():
    # Root node
    root_ = SimpleNode(key=0)
    
    # Level 1
    n1_ = SimpleNode(key=1, parent=root_)
    n2_ = SimpleNode(key=2, parent=root_)
    
    # Level 2
    n3_ = SimpleNode(key=3, parent=n1_)
    n4_ = SimpleNode(key=4, parent=n1_)
    n5_ = SimpleNode(key=5, parent=n2_)
    
    # Level 3
    n6_ = SimpleNode(key=6, parent=n3_)
    n7_ = SimpleNode(key=7, parent=n3_)
    n8_ = SimpleNode(key=8, parent=n4_)
    
    return root_, {
        0: root_, 1: n1_, 2: n2_, 
        3: n3_, 4: n4_, 5: n5_, 
        6: n6_, 7: n7_, 8: n8_
    }

class TestTreePathfinding:
    root_, nodes = build_sample_tree()

    def test_get_path_to_node_simple(self):
        # Test path from root to a deep node (e.g., n7)
        # Path: 0 -> 1 -> 3 -> 7
        node_7 = self.nodes[7]
        expected_path_keys = [0, 1, 3, 7]
        actual_path_keys = [n.key for n in reverse_path_iterator(node_7)][::-1]
        assert actual_path_keys == expected_path_keys, "Path from root to node 7 failed"

        # Test path to a nearby node (e.g., n4)
        # Path: 0 -> 1 -> 4
        node_4 = self.nodes[4]
        expected_path_keys = [0, 1, 4]
        actual_path_keys = [n.key for n in reverse_path_iterator(node_4)][::-1]
        assert actual_path_keys == expected_path_keys, "Path from root to node 4 failed"

    def test_get_path_non_existent(self):
        # a node from another tree does not have the root on its path
        dummy_node = SimpleNode(key=999)
        assert all(n is not self.root_ for n in reverse_path_iterator(dummy_node))
        assert list(reverse_path_iterator(dummy_node)) == [dummy_node]
