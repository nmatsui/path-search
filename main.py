#!/usr/bin/env python
from importlib import import_module
import sys
import images
from data import Node, Edge
from searcher import Astar, Dijkstra
from fast_astar import Astar2
import time

from typing import List, Dict, Tuple

if len(sys.argv) != 2:
    print(f'usage: {sys.argv[0]} module_name')
    sys.exit(1)

graph = import_module(sys.argv[1])
SIZE: Tuple[int, int] = graph.SIZE  # type: ignore
NODES: Dict[str, Node] = graph.NODES  # type: ignore
EDGES: List[Edge] = graph.EDGES  # type: ignore
START_NODE: Node = graph.START_NODE  # type: ignore
GOAL_NODE: Node = graph.GOAL_NODE  # type: ignore


for node in NODES.values():
    node.edges = [edge for edge in EDGES if edge.st == node or edge.ed == node]


GRAPH_NAME = 'graph.jpg'
ASTAR_PATH_NAME = 'astar_path.jpg'
DIJKSTRA_PATH_NAME = 'dijkstra_path.jpg'
FAST_ASTAR_NAME = 'fast_astar_path.jpg'


def main() -> None:
    print('start')

    a1s = time.time()
    astar_path = Astar(START_NODE, GOAL_NODE).calculate()
    print(f'save astar path to {ASTAR_PATH_NAME}, time={time.time() - a1s}')
    images.draw_path(ASTAR_PATH_NAME, SIZE, NODES, EDGES, astar_path)

    d1s = time.time()
    dijkstra_path = Dijkstra(START_NODE, GOAL_NODE).calculate()
    print(f'save dijkstra path to {DIJKSTRA_PATH_NAME}, time={time.time() - d1s}')
    images.draw_path(DIJKSTRA_PATH_NAME, SIZE, NODES, EDGES, dijkstra_path)

    a2s = time.time()
    astar_path = Astar2(START_NODE, GOAL_NODE).calculate()
    print(f'save fast astar path to {FAST_ASTAR_NAME}, time={time.time() - a2s}')
    images.draw_path(FAST_ASTAR_NAME, SIZE, NODES, EDGES, astar_path)


if __name__ == '__main__':
    main()
