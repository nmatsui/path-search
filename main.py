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

GRAPH_NAME = 'graph.jpg'
ASTAR_PATH_NAME = 'astar_path.jpg'
DIJKSTRA_PATH_NAME = 'dijkstra_path.jpg'
FAST_ASTAR_NAME = 'fast_astar_path.jpg'


def prepare_graph(module_name: str) -> Tuple[Tuple[int, int], Dict[str, Node], List[Edge], Node, Node]:
    graph = import_module(sys.argv[1])
    size: Tuple[int, int] = graph.SIZE  # type: ignore
    nodes: Dict[str, Node] = graph.NODES  # type: ignore
    edges: List[Edge] = graph.EDGES  # type: ignore
    start_node: Node = graph.START_NODE  # type: ignore
    goal_node: Node = graph.GOAL_NODE  # type: ignore

    for node in nodes.values():
        node.edges = [edge for edge in edges if edge.st == node or edge.ed == node]

    return size, nodes, edges, start_node, goal_node


def main() -> None:
    print('## start ##')

    print('prepare graph')
    size, nodes, edges, start_node, goal_node = prepare_graph(sys.argv[1])

    print('start searching by Astar algorithm')
    a1s = time.time()
    astar_path = Astar(start_node, goal_node).calculate()
    print(f'finish astar searching and save searched path as {ASTAR_PATH_NAME}, time={time.time() - a1s}')
    images.draw_path(ASTAR_PATH_NAME, size, nodes, edges, astar_path)

    print('start searching by Dijkstra algorithm')
    d1s = time.time()
    dijkstra_path = Dijkstra(start_node, goal_node).calculate()
    print(f'finish dijkstra searching and save searched path as {DIJKSTRA_PATH_NAME}, time={time.time() - d1s}')
    images.draw_path(DIJKSTRA_PATH_NAME, size, nodes, edges, dijkstra_path)

    print('start searching by Fast Astar algorithm')
    a2s = time.time()
    fast_astar_path = Astar2(start_node, goal_node).calculate()
    print(f'finish searching and save searched path as {FAST_ASTAR_NAME}, time={time.time() - a2s}')
    images.draw_path(FAST_ASTAR_NAME, size, nodes, edges, fast_astar_path)

    print('## end ##')


if __name__ == '__main__':
    main()
