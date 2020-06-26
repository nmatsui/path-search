from dataclasses import dataclass, field
from data import Node
from typing import List, Optional


@dataclass
class AstarNode:
    node: Node
    goal: Node = field(repr=False)
    fs: float = 0.0
    gs: float = 0.0
    parent: Optional['AstarNode'] = field(default=None, repr=False)
    _nexts: Optional[List['AstarNode']] = field(default=None, repr=False)

    @property
    def x(self) -> int:
        return self.node.x

    @property
    def y(self) -> int:
        return self.node.y

    @property
    def nexts(self) -> List['AstarNode']:
        if self._nexts is None:
            self._nexts = [AstarNode(edge.get_opposite_node(self.node), self.goal) for edge in self.node.edges]
        return self._nexts

    @property
    def hs(self) -> float:
        return (self.x - self.goal.x)**2 + (self.y - self.goal.y)**2

    @property
    def is_goal(self) -> bool:
        return self.node == self.goal


class Astar:
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.goal = goal
        self.open_list: List[AstarNode] = []
        self.close_list: List[AstarNode] = []

    def calculate(self) -> List[Node]:
        start = AstarNode(self.start, self.goal)
        start.fs = start.hs
        self.open_list.append(start)
        end: Optional[AstarNode] = None

        while True:
            if len(self.open_list) == 0:
                print('No route found')
                return []

            target: AstarNode = min(self.open_list, key=lambda x: x.fs)
            if target.is_goal:
                end = target
                break

            self.open_list.remove(target)
            self.close_list.append(target)

            target.gs = target.fs - target.hs

            for candidate in target.nexts:
                fs = target.gs + self._cost(target, candidate) + candidate.hs

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

    def _cost(self, target: AstarNode, candidate: AstarNode) -> float:
        return (candidate.x - target.x)**2 + (candidate.y - target.y)**2

    def _find_candidate(self, li: List[AstarNode], candidate: AstarNode) -> Optional[AstarNode]:
        try:
            return next(filter(lambda e: e.x == candidate.x and e.y == candidate.y, li))
        except StopIteration:
            return None
