from PIL import Image, ImageDraw
from data import Node, Edge

from typing import Tuple, Dict, List

BG_COLOR = (255, 255, 255)

NODE_R = 4
NODE_COLOR = (0, 0, 255)

EDGE_COLOR = (0, 0, 0)

PATH_WIDTH = 3
PATH_COLOR = (255, 0, 0)


def __create_baseimage(size: Tuple, bg_color: Tuple, nodes: Dict[str, Node], edges: List[Edge]) -> Image:
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    for node in nodes.values():
        draw.ellipse((node.x - NODE_R, node.y - NODE_R, node.x + NODE_R, node.y + NODE_R), fill=NODE_COLOR)
    for edge in edges:
        draw.line((edge.st.as_tuple(), edge.ed.as_tuple()), fill=EDGE_COLOR)
    return img


def draw_graph(filename: str, size: Tuple[int, int], nodes: Dict[str, Node], edges: List[Edge]) -> None:
    img = __create_baseimage(size, BG_COLOR, nodes, edges)
    img.save(filename)


def draw_path(filename: str, size: Tuple[int, int], nodes: Dict[str, Node], edges: List[Edge], path: List[Node]) -> None:
    points = [node.as_tuple() for node in path]

    img = __create_baseimage(size, BG_COLOR, nodes, edges)
    draw = ImageDraw.Draw(img)
    draw.line(points, fill=PATH_COLOR, width=PATH_WIDTH)
    img.save(filename)
