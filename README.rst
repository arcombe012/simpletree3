Simpletree3 module
==================

Offers classes implementing basic tree-like
functionality, as well as iterators for walking
the trees and node search functionality. Requires Python3.4 or later.
Cython compilation is performed if cython is installed.

The design goal is to provide a basic class implementing the
essential tree structure and functionality. Practical applications will
want to inherit from one of the provided classes
in order to provide custom functionality. Tree walking
algorithms are implemented as generators, in order to
minimize the use of temporary objects and focus on
speed and efficiency.

Classes
-------

Two classes are provided: *SimpleNode* and
*FlexibleNode*.

SimpleNode
^^^^^^^^^^

This is the base class that provides the
tree node functionality by connecting
parents to children. Additional functionality
can be added by deriving from *SimpleNode*.

Each node is identified by a *key* parameter
of an arbitrary hashable type. Node keys must be unique
among the direct children of a node, since node
children are held in a dict using the key attribute as
dictionary keys (hence the hashable requirement).

Connections with nodes up and down the tree are
accessed through the parent and children properties
(children offers an iterator for the child nodes,
sorted by node key).
The root node of a tree is the node with parent
equal to None. Setting the parent of a node
checks that no loops are inserted and adds
the current node to the parent's children (if needed).
Deleting a parent sets it to None and removes
the node from the parent's children.

Some additional convenience properties are defined -
siblings, ancestors, depth, height - as well as
methods for adding and removing child nodes.

FlexibleNode
^^^^^^^^^^^^
This is a convenience class that add hooks to
setting and deleting a parent. The motivation for
providing it is that currently Python does not
offer a simple syntax for calling a base class
property from a derived class when that property is
overriden, so by inheriting from *FlexibleNode*
instead of *SimpleNode* one only has to override
the hooks to perform any desired operations.
Adding and deleting children can be
directly overriden, since they are not implemented
as properties. The design decision of having the
hook functionality implemented in a separate class
allows one to choose the trade-off between
speed and flexibility of tree building
(important for very large trees).


Iterators
---------

The module implements preorder, postorder, level
and leaf iterators. Each comes in two flavors - a simple
one, iterating through all nodes, and a filtered
one, where specific nodes can be selected
and/or specific subtrees can be ignored.

Search functionality
--------------------

The simplest search is done using a preorder iteration
procedure that yields nodes with the specified key.
A separate find function returns the first node matching
that key.

A common use case when building trees is that
subsequent nodes are added in a subtree containing the last
inserted node. To optimize for this case, a separate
search procedure is implemented, which walks up the
tree from the start node and searches for the
specified key in the subtree rooted in each ancestor.
