#!/usr/bin/env python
from importlib import import_module
import sys
import images
from data import Node, Edge
from routes import Astar

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
PATH_NAME = 'path.jpg'


def main() -> None:
    print('start')

    images.draw_graph(GRAPH_NAME, SIZE, NODES, EDGES)
    print(f'save graph to {GRAPH_NAME}')

    path = Astar(START_NODE, GOAL_NODE).calculate()
    images.draw_path(PATH_NAME, SIZE, NODES, EDGES, path)
    print(f'save path to {PATH_NAME}')


if __name__ == '__main__':
    main()
