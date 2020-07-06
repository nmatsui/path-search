import math
import heapq
from dataclasses import dataclass, field
from enum import Enum, auto
from data import Node
from typing import List, Dict, Tuple, Optional, ClassVar


class NodeType(Enum):
    NEW = auto()
    OPEN = auto()
    CLOSE = auto()


@dataclass
class CalcNode:
    cnt: ClassVar[int] = 0
    cache: ClassVar[Dict[Tuple[int, int], 'CalcNode']] = {}

    @classmethod
    def new(cls, node: Node):
        if node.as_tuple() not in cls.cache:
            cls.cache[node.as_tuple()] = CalcNode(node)
        return cls.cache[node.as_tuple()]

    node: Node
    id: int = 0
    fs: float = 0.0
    gs: float = 0.0
    nodetype: NodeType = NodeType.NEW
    parent: Optional['CalcNode'] = field(default=None, repr=False)
    _nexts: Optional[List['CalcNode']] = field(default=None, repr=False)

    def __post_init__(self, *args, **kwargs):
        self.id = CalcNode.cnt
        CalcNode.cnt += 1

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

    def __iter__(self):
        current = self
        while current is not None:
            yield current
            current = current.parent


class FastAstar:
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.goal = goal

    def calculate(self) -> List[Node]:
        target: CalcNode
        table: Dict[int, CalcNode] = {}
        open_list: List[Tuple[float, int]] = []
        heapq.heapify(open_list)

        start = CalcNode.new(self.start)
        start.fs = self._hs(start)

        table[start.id] = start
        heapq.heappush(open_list, (start.fs, start.id))

        while True:
            if len(open_list) == 0:
                print('No route found')
                return []

            target = table[heapq.heappop(open_list)[1]]
            if target.nodetype == NodeType.CLOSE:
                continue

            if target.node == self.goal:
                break

            target.nodetype = NodeType.CLOSE

            target.gs = target.fs - self._hs(target)

            for candidate in target.nexts:
                fs = target.gs + self._cost(target, candidate) + self._hs(candidate)

                if candidate.nodetype == NodeType.NEW:
                    candidate.fs = fs
                    candidate.parent = target
                    candidate.nodetype = NodeType.OPEN
                    table[candidate.id] = candidate
                    heapq.heappush(open_list, (candidate.fs, candidate.id))
                else:
                    if fs < candidate.fs:
                        candidate.fs = fs
                        candidate.parent = target
                        candidate.nodetype = NodeType.OPEN
                        table[candidate.id] = candidate
                        heapq.heappush(open_list, (candidate.fs, candidate.id))

        return [li.node for li in reversed(list(target))]

    def _cost(self, target: CalcNode, candidate: CalcNode) -> float:
        return math.sqrt((candidate.x - target.x)**2 + (candidate.y - target.y)**2)

    def _hs(self, node: CalcNode) -> float:
        return math.sqrt((node.x - self.goal.x)**2 + (node.y - self.goal.y)**2)
