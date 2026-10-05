from collections.abc import Generator, Hashable
from operator import itemgetter

from .abstract_node import AbstractNode
from .algorithms import count_nodes, reverse_path_iterator


class SimpleNode(AbstractNode):
    """
    A simple node base class used for tree building.
    It requires at minimum a key and a parent.
    The children of a given node are stored in a dict
    with their keys as dictionary keys, so they must be unique
    (repetition of keys is allowed for different nodes' children)

    Children are iterated sorted by key, which requires the keys of sibling
    nodes to be mutually comparable. Subclasses can set ``sort_children = False``
    to iterate the children in insertion order instead (faster, and works with
    keys of mixed types).
    """
    sort_children: bool = True

    def __init__(self, key: Hashable, parent: "SimpleNode | None" = None, **kwargs):
        for name_ in kwargs:
            if name_.startswith("_SimpleNode__"):
                raise InvalidNodeOperation(f"overwriting internal attribute {name_}")
        self.__parent: SimpleNode | None = None
        self.__children: dict[Hashable, SimpleNode] = {}
        self.__key: Hashable = key
        if parent is not None:
            self.parent = parent
        self.__dict__.update(kwargs)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(key={self.__key!r}, children={len(self.__children)})"

    @property
    def key(self):
        """return the node's key."""
        return self.__key

    @key.setter
    def key(self, other: Hashable):
        """setting the key outside the constructor is forbidden."""
        raise InvalidNodeOperation("setting the node key")

    @key.deleter
    def key(self):
        """deleting the key is forbidden."""
        raise InvalidNodeOperation("deleting the node key")

    @property
    def parent(self) -> "SimpleNode | None":
        """return the parent node."""
        return self.__parent

    @parent.setter
    def parent(self, other: "SimpleNode | None"):
        """set the parent node.
        If not None, ensure that self is a child of the new parent.
        All checks are performed before the tree is modified,
        so a failed assignment leaves the tree unchanged."""
        if self.__parent is other:
            # already has this parent
            return
        if other is not None:
            if self is other:
                raise InvalidNodeOperation("attempting to insert node as child of itself")
            # a leaf cannot be an ancestor of other, so skip the walk to the root
            # (this keeps the usual building of trees from new nodes O(1) per node)
            if self.__children and any(n_ is self for n_ in reverse_path_iterator(other)):
                raise InvalidNodeOperation("attempting to insert ancestor node as child")
            if self.__key in other.__children:
                raise DuplicateChildNode(key=self.__key)
        if self.__parent is not None:
            self.__parent.__children.pop(self.__key, None)
        if other is not None:
            other.__children[self.__key] = self
        self.__parent = other

    @parent.deleter
    def parent(self):
        """deleting the parent detaches the node from its parent."""
        self._detach()

    def _detach(self):
        """remove self from the parent's children and set the parent to None.
        All the removal operations go through here."""
        if self.__parent is not None:
            self.__parent.__children.pop(self.__key, None)
            self.__parent = None

    def detach(self):
        """detach self (and its subtree) from the parent, making self a root node."""
        self._detach()

    def has_child(self, key):
        """check if the key belongs to one of the children"""
        return key in self.__children

    def add_child(self, child):
        """add a child. Set self as the child's parent, if needed."""
        if self is child:
            raise InvalidNodeOperation("adding itself as child")
        key = child.key
        old_child = self.__children.get(key, None)
        if old_child is child:
            # already have it as child
            return
        if old_child is not None:
            # already have a different child node with this key
            raise DuplicateChildNode(key=key)
        child.parent = self

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
        if key is None:
            return None
        child_ = self.__children.get(key)
        if child_ is None:
            return None
        child_._detach()
        if recursive:
            child_.remove_children(recursive=True)
            return None
        return child_

    def remove_children(self, recursive: bool = False):
        """
        :param recursive: whether to recursively remove all descendants
        :return: a list of the former children, or None if recursive (or if no children)
        """
        if not self.__children:
            return None
        if recursive:
            # iterative, so that deep subtrees do not hit the recursion limit
            stack_ = [self]
            while stack_:
                kids_ = list(stack_.pop().__children.values())
                for k_ in kids_:
                    k_._detach()
                stack_.extend(kids_)
            return None
        kids_ = list(self.__children.values())
        for k_ in kids_:
            k_._detach()
        return kids_

    def child(self, key) -> "SimpleNode | None":
        return self.__children.get(key, None)

    def get_descendant(self, *keys) -> "SimpleNode | None":
        """walk down the tree following the given keys, one per level.
        Return the node found, or None if the path does not exist.
        With no keys, return self."""
        node_ = self
        for key_ in keys:
            next_ = node_.__children.get(key_)
            if next_ is None:
                return None
            node_ = next_
        return node_

    @property
    def children(self) -> "Generator[SimpleNode, None, None]":
        """iterate through the node's children, sorted by key
        (or in insertion order, if sort_children is False)"""
        if self.sort_children:
            yield from (v for _, v in sorted(self.__children.items(), key=itemgetter(0)))
        else:
            yield from list(self.__children.values())

    @property
    def children_count(self):
        """return the number of children."""
        return len(self.__children)

    @property
    def siblings(self):
        """iterate through the node's siblings if any."""
        if self.__parent is not None:
            yield from (v for v in self.__parent.children if v is not self)

    @property
    def siblings_count(self):
        """count the node's siblings"""
        if self.__parent is not None:
            return self.__parent.children_count - 1
        return 0

    @property
    def ancestors(self):
        """return a tuple of ancestors, starting from the root node"""
        if self.__parent is not None:
            return tuple(reversed(list(reverse_path_iterator(self.__parent))))
        return ()

    @property
    def path(self):
        """return a tuple of nodes from the root node down to self (inclusive)"""
        return tuple(reversed(list(reverse_path_iterator(self))))

    @property
    def key_path(self):
        """return a tuple of the keys of the nodes from the root node down to self"""
        return tuple(n_.key for n_ in self.path)

    @property
    def root(self) -> "SimpleNode":
        """return the root node of the tree containing self"""
        node_ = self
        while node_.__parent is not None:
            node_ = node_.__parent
        return node_

    @property
    def is_root(self) -> bool:
        """check whether self is a root node"""
        return self.__parent is None

    @property
    def is_leaf(self) -> bool:
        """check whether self is a leaf node"""
        return not self.__children

    def is_ancestor_of(self, other: "SimpleNode") -> bool:
        """check whether self is a (strict) ancestor of other"""
        node_ = other.__parent
        while node_ is not None:
            if node_ is self:
                return True
            node_ = node_.__parent
        return False

    def is_descendant_of(self, other: "SimpleNode") -> bool:
        """check whether self is a (strict) descendant of other"""
        return other.is_ancestor_of(self)

    @property
    def height(self) -> int:
        """return the height of the subtree rooted on self
        (a.k.a. the longest branch)"""
        height_ = -1
        level_ = [self]
        while level_:
            height_ += 1
            level_ = [c_ for n_ in level_ for c_ in n_.__children.values()]
        return height_

    @property
    def depth(self):
        """return the depth of self in the tree
        (the distance/number of edges to the root node)"""
        return sum(1 for _ in reverse_path_iterator(self)) - 1

    @property
    def size(self) -> int:
        """return the number of nodes in the subtree rooted on self (including self)"""
        return count_nodes(self)


class FlexibleNode(SimpleNode):
    """
    A class derived from the simple node
    that allows hooks before and after setting and/or
    deleting a parent node.
    Provided explicitly for convenience, since so far there is no
    simple syntax for overriding properties from a base class.

    The assign hooks are called when setting the parent (possibly to None),
    the delete hooks whenever the node is detached from its parent
    (``del node.parent``, ``detach()``, ``remove_child()``, ``remove_children()``).

    Note that SimpleNode calls the parent setter for non-None parents in __init__,
    so if the inherited hooks set any attributes in the derived class
    they will be set when calling super().__init__(...)
    so don't reset them after that call unless necessary
    """
    @property  # type: ignore[override]
    def parent(self) -> "FlexibleNode | None":
        """override the parent getter from the base class"""
        return SimpleNode.parent.fget(self)  # type: ignore

    @parent.setter
    def parent(self, other):
        """override the parent setter to allow for hooks
        before and after adding the parent"""
        self._pre_assign_parent_hook(other)
        SimpleNode.parent.fset(self, other)  # type: ignore
        self._post_assign_parent_hook(other)

    @parent.deleter
    def parent(self):
        """override the parent deleter from the base class
        to allow for hooks before and after deletion"""
        self._detach()

    def _detach(self):
        """wrap the detaching of the node with the delete hooks"""
        self._pre_delete_parent_hook()
        super()._detach()
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
    pass


class DuplicateChildNode(SimpleTreeException):
    def __init__(self, key):
        super().__init__(f"Attempting to add a duplicate child with key {key}")
        self.key = key


class InvalidNodeOperation(SimpleTreeException):
    def __init__(self, operation):
        super().__init__(f"invalid operation: {operation}")
