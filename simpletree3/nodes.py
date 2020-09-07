# cython: language_level = 3
from functools import lru_cache

from .algorithms import reverse_path_iterator


class SimpleNode:
    """
    A simple node base class used for tree building.
    It requires at minimum a key and a parent.
    The children of a given node are stored in a dict
    with their keys as dictionary keys, so they must be unique
    (repetition of keys is allowed for different nodes' children)
    """
    def __init__(self, key, parent=None, **kwargs):
        self.__parent = None
        self.__children = dict()
        self.__key = key
        if parent:      # pragma: no branch
            self.parent = parent
        self.__dict__.update(kwargs)

    @property
    def key(self):
        """return the node's key."""
        return self.__key

    @key.setter
    def key(self, other):
        """setting the key outside the constructor is forbidden."""
        raise InvalidNodeOperation("setting the node key")

    @key.deleter
    def key(self):
        """deleting the key is forbidden."""
        raise InvalidNodeOperation("deleting the node key")

    @property
    def parent(self):
        """return the parent node."""
        return self.__parent

    @parent.setter
    def parent(self, other):
        """set the parent node.
        If not null, ensure that self is a child of the new parent"""
        if self.__parent == other:
            # already has this parent
            return
        self.__parent = other
        if other:       # pragma: no branch
            if self in reverse_path_iterator(other):        # pragma: no branch
                if self is other:       # pragma: no branch
                    raise InvalidNodeOperation("attempting to insert node as child of itself")
                raise InvalidNodeOperation("attempting to insert ancestor node as child")
            other.add_child(self)

    @parent.deleter
    def parent(self):
        """deleting the parent sets it to None."""
        self.__parent = None

    def has_child(self, key):
        """check if the key belongs to one of the children"""
        return key in self.__children.keys()

    def add_child(self, child):
        """add a child. Set self as the child's parent, if needed."""
        if self == child:       # pragma: no branch
            raise InvalidNodeOperation("adding itself as child")
        if child.parent != self:        # pragma: no branch
            child.parent = self
        key = child.key
        old_child = self.__children.get(key, None)
        if old_child is None:       # pragma: no branch
            # new child
            self.__children[key] = child
            return
        if old_child == child:       # pragma: no branch
            # already have it as child
            return
        # already have a different child node with this key
        raise DuplicateChildNode(key=key)

    def remove_child(self, key, recursive: bool = False):
        """
        :param key: key of the child node to remove
        :param recursive: whether to recursively remove the descendants of the child node
        :return: the removed child node, or None if recursive requested (or if invalid key)
        removes a child node by key.
        if key is None, do nothing.
        if the child node has children and recursive is specified,
        dismantle all the structure of the subtree rooted in the child node.
        returns the removed child, unless recursive is specified, in which case
        it deletes all the nodes of the subtree
        """
        if key is None or key not in self.__children.keys():        # pragma: no branch
            return None
        child_ = self.__children.pop(key)
        child_.parent = None
        if recursive:
            child_.remove_children(recursive=True)
            del child_
            return None
        else:
            return child_

    def remove_children(self, recursive: bool = False):
        """
        :param recursive: whether to recursively remove all descendants
        :return: a list of the former children, or None if recursive (or if no children)
        """
        if not self.__children:        # pragma: no branch
            return None
        if recursive:
            while self.__children:
                k_, v_ = self.__children.popitem()
                v_.parent = None
                v_.remove_children(recursive=True)
                del v_
            return None
        else:
            kids_ = list(self.__children.values())
            self.__children.clear()
            for k_ in kids_:
                k_.parent = None
            return kids_

    def child(self, key):
        return self.__children.get(key, None)

    @property
    def children(self):
        """iterate through the node's children, sorted by key"""
        yield from (v for _, v in sorted(self.__children.items()))

    @property
    def children_count(self):
        """return the number of children."""
        return len(self.__children)

    @property
    def siblings(self):
        """iterate through the node's siblings if any."""
        if self.__parent:       # pragma: no branch
            yield from (v for v in self.__parent.children
                if v.key != self.key)

    @property
    def siblings_count(self):
        """count the node's siblings"""
        if self.__parent:       # pragma: no branch
            return self.__parent.children_count - 1
        return 0

    @property
    def ancestors(self):
        """return a tuple of ancestors, starting from the root node"""
        if self.__parent:       # pragma: no branch
            return tuple(reversed(list(reverse_path_iterator(self.__parent))))
        return tuple()

    @property
    def is_root(self) -> bool:
        """check whether self is a root node"""
        return self.__parent is None

    @property
    def is_leaf(self) -> bool:
        """check whether self is a leaf node"""
        return not self.__children

    @property
    @lru_cache()
    def height(self) -> int:
        """return the height of the subtree rooted on self
        (a.k.a. the longest branch)"""
        if self.__children:        # pragma: no branch
            return 1 + max(child.height for child in self.__children.values())
        return 0

    @property
    @lru_cache()
    def depth(self):
        """return the depth of self in the tree
        (the distance/number of edges to the root node)"""
        if self.__parent:       # pragma: no branch
            return self.__parent.depth + 1
        return 0


class FlexibleNode(SimpleNode):
    """
    A class derived from the simple node
    that allows hooks before and after setting and/or
    deleting a parent node.
    Provided explicitly for convenience, since so far there is no
    simple syntax for overriding properties from a base class.

    Note that SimpleNode calls the parent setter for non-None parents in __init__,
    so if the inherited hooks set any attributes in the derived class
    they will be set when calling super().__init__(...)
    so don't reset them after that call unless necessary
    """
    def __init__(self, key, parent=None, **kwargs):
        super().__init__(key, parent=parent, **kwargs)

    @property
    def parent(self):
        """override the parent getter from the base class"""
        return SimpleNode.parent.fget(self)

    @parent.setter
    def parent(self, other):
        """override the parent setter to allow for hooks
        before and after adding the parent"""
        self._pre_assign_parent_hook(other)
        SimpleNode.parent.fset(self, other)
        self._post_assign_parent_hook(other)

    @parent.deleter
    def parent(self):
        """override the parent deleter from the base class
        to allow for hooks before and after deletion"""
        self._pre_delete_parent_hook()
        SimpleNode.parent.fdel(self)
        self._post_delete_parent_hook()

    def _pre_assign_parent_hook(self, other):
        pass

    def _post_assign_parent_hook(self, other):
        pass

    def _pre_delete_parent_hook(self):
        pass

    def _post_delete_parent_hook(self):
        pass


class SimpleTreeException(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)


class DuplicateChildNode(SimpleTreeException):
    def __init__(self, key):
        super().__init__("Attempting to add a duplicate child with key {}".format(key))


class InvalidNodeOperation(SimpleTreeException):
    def __init__(self, operation):
        super().__init__("invalid operation: {}".format(operation))
