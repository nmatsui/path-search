from dataclasses import dataclass

@dataclass
class Node:
  x: int
  y: int

  def as_tuple(self):
    return (self.x, self.y)


@dataclass
class Edge:
  st: Node
  ed: Node