import math
import heapq
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from data import Node
from typing import List, Optional, Any


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

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, CalcNode):
            return NotImplemented
        return self.fs < other.fs

    def __iter__(self):
        current = self
        while current is not None:
            yield current
            current = current.parent


class Searcher(metaclass=ABCMeta):
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.goal = goal
        self.open_list: List[CalcNode] = []
        self.close_list: List[CalcNode] = []
        heapq.heapify(self.open_list)

    def calculate(self) -> List[Node]:
        start = CalcNode(self.start)
        start.fs = self._hs(start)
        heapq.heappush(self.open_list, start)
        target: CalcNode

        while True:
            if len(self.open_list) == 0:
                print('No route found')
                return []

            target = heapq.heappop(self.open_list)
            if target.node == self.goal:
                break

            self.close_list.append(target)

            target.gs = target.fs - self._hs(target)

            for candidate in target.nexts:
                fs = target.gs + self._cost(target, candidate) + self._hs(candidate)

                opened_candidate = self._find_candidate(self.open_list, candidate)
                if opened_candidate is not None:
                    if fs < opened_candidate.fs:
                        self.open_list.remove(opened_candidate)
                        opened_candidate.fs = fs
                        opened_candidate.parent = target
                        heapq.heappush(self.open_list, opened_candidate)
                else:
                    closed_candidate = self._find_candidate(self.close_list, candidate)
                    if closed_candidate is not None:
                        if fs < closed_candidate.fs:
                            self.close_list.remove(closed_candidate)
                            closed_candidate.fs = fs
                            closed_candidate.parent = target
                            heapq.heappush(self.open_list, closed_candidate)
                    else:
                        candidate.fs = fs
                        candidate.parent = target
                        heapq.heappush(self.open_list, candidate)

        return [li.node for li in reversed(list(target))]

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
