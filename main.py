#!/usr/bin/env python
from importlib import import_module
import sys
import images
from data import Node, Edge
from routes import Astar, Dijkstra

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


def main() -> None:
    print('start')

    images.draw_graph(GRAPH_NAME, SIZE, NODES, EDGES)
    print(f'save graph to {GRAPH_NAME}')

    astar_path = Astar(START_NODE, GOAL_NODE).calculate()
    images.draw_path(ASTAR_PATH_NAME, SIZE, NODES, EDGES, astar_path)
    print(f'save astar path to {ASTAR_PATH_NAME}')

    dijkstra_path = Dijkstra(START_NODE, GOAL_NODE).calculate()
    images.draw_path(DIJKSTRA_PATH_NAME, SIZE, NODES, EDGES, dijkstra_path)
    print(f'save dijkstra path to {DIJKSTRA_PATH_NAME}')


if __name__ == '__main__':
    main()
