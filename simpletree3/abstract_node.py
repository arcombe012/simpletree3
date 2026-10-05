from abc import ABCMeta, abstractmethod
from collections.abc import Hashable, Iterator


class AbstractNode(metaclass=ABCMeta):
    @property
    @abstractmethod
    def key(self) -> Hashable:
        pass

    @property
    @abstractmethod
    def parent(self) -> "AbstractNode | None":
        pass

    @property
    @abstractmethod
    def children(self) -> "Iterator[AbstractNode]":
        pass

    @property
    @abstractmethod
    def children_count(self) -> int:
        pass
