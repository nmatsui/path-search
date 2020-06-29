import math
import heapq
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from data import Node
from typing import List, Dict, Tuple, Optional, Any, ClassVar


@dataclass
class CalcNode:
    cache: ClassVar[Dict[Tuple[int, int], 'CalcNode']] = {}

    @classmethod
    def new(cls, node: Node):
        if node.as_tuple() not in cls.cache:
            cls.cache[node.as_tuple()] = CalcNode(node)
        return cls.cache[node.as_tuple()]

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
            self._nexts = [CalcNode.new(edge.get_opposite_node(self.node)) for edge in self.node.edges]
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

    def calculate(self) -> List[Node]:
        target: CalcNode

        open_list: List[CalcNode] = []
        close_list: List[CalcNode] = []
        heapq.heapify(open_list)

        start = CalcNode.new(self.start)
        start.fs = self._hs(start)

        heapq.heappush(open_list, start)

        while True:
            if len(open_list) == 0:
                print('No route found')
                return []

            target = heapq.heappop(open_list)
            if target.node == self.goal:
                break

            close_list.append(target)

            target.gs = target.fs - self._hs(target)

            for candidate in target.nexts:
                fs = target.gs + self._cost(target, candidate) + self._hs(candidate)

                opened_candidate = self._find_candidate(open_list, candidate)
                if opened_candidate is not None:
                    if fs < opened_candidate.fs:
                        open_list.remove(opened_candidate)
                        opened_candidate.fs = fs
                        opened_candidate.parent = target
                        heapq.heappush(open_list, opened_candidate)
                else:
                    closed_candidate = self._find_candidate(close_list, candidate)
                    if closed_candidate is not None:
                        if fs < closed_candidate.fs:
                            close_list.remove(closed_candidate)
                            closed_candidate.fs = fs
                            closed_candidate.parent = target
                            heapq.heappush(open_list, closed_candidate)
                    else:
                        candidate.fs = fs
                        candidate.parent = target
                        heapq.heappush(open_list, candidate)

        return [li.node for li in reversed(list(target))]

    def _cost(self, target: CalcNode, candidate: CalcNode) -> float:
        return math.sqrt((candidate.x - target.x)**2 + (candidate.y - target.y)**2)

    def _find_candidate(self, li: List[CalcNode], candidate: CalcNode) -> Optional[CalcNode]:
        try:
            return li[li.index(candidate)]
        except ValueError:
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
