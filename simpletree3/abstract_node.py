from typing import Hashable, Generator
from abc import ABCMeta, abstractmethod, abstractproperty


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
    def children(self) -> "Generator[AbstractNode, None, None]":
        pass

    @property
    @abstractmethod
    def children_count(self) -> int:
        pass
