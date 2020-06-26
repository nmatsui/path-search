import math
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from data import Node
from typing import List, Optional


@dataclass
class CalcNode:
    node: Node
    fs: float = 0.0
    gs: float = 0.0
    parent: Optional['CalcNode'] = field(default=None, repr=False)
    _nexts: Optional[List['CalcNode']] = field(default=None, repr=False)

    @property
    def x(self) -> int:
        return self.node.x

    @property
    def y(self) -> int:
        return self.node.y

    @property
    def nexts(self) -> List['CalcNode']:
        if self._nexts is None:
            self._nexts = [CalcNode(edge.get_opposite_node(self.node)) for edge in self.node.edges]
        return self._nexts


class Searcher(metaclass=ABCMeta):
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.goal = goal
        self.open_list: List[CalcNode] = []
        self.close_list: List[CalcNode] = []

    def calculate(self) -> List[Node]:
        start = CalcNode(self.start)
        start.fs = self._hs(start)
        self.open_list.append(start)
        end: Optional[CalcNode] = None

        while True:
            if len(self.open_list) == 0:
                print('No route found')
                return []

            target: CalcNode = min(self.open_list, key=lambda x: x.fs)
            if target.node == self.goal:
                end = target
                break

            self.open_list.remove(target)
            self.close_list.append(target)

            target.gs = target.fs - self._hs(target)

            for candidate in target.nexts:
                fs = target.gs + self._cost(target, candidate) + self._hs(candidate)

                opened_candidate = self._find_candidate(self.open_list, candidate)
                if opened_candidate is not None:
                    if opened_candidate.fs > fs:
                        opened_candidate.fs = fs
                        opened_candidate.parent = target
                else:
                    closed_candidate = self._find_candidate(self.close_list, candidate)
                    if closed_candidate is not None:
                        if closed_candidate.fs > fs:
                            closed_candidate.fs = fs
                            closed_candidate.parent = target
                            self.close_list.remove(closed_candidate)
                            self.open_list.append(closed_candidate)
                    else:
                        candidate.fs = fs
                        candidate.parent = target
                        self.open_list.append(candidate)

        result: List[Node] = []
        while True:
            result.insert(0, end.node)
            if end.parent is None:
                break
            end = end.parent

        return result

    def _cost(self, target: CalcNode, candidate: CalcNode) -> float:
        return math.sqrt((candidate.x - target.x)**2 + (candidate.y - target.y)**2)

    def _find_candidate(self, li: List[CalcNode], candidate: CalcNode) -> Optional[CalcNode]:
        try:
            return next(filter(lambda e: e.x == candidate.x and e.y == candidate.y, li))
        except StopIteration:
            return None

    @abstractmethod
    def _hs(self, node: CalcNode) -> float:
        raise NotImplementedError


class Astar(Searcher):
    def _hs(self, node: CalcNode) -> float:
        return math.sqrt((node.x - self.goal.x)**2 + (node.y - self.goal.y)**2)


class Dijkstra(Searcher):
    def _hs(self, node: CalcNode) -> float:
        return 0.0
