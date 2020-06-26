from PIL import Image, ImageDraw

SIZE = (500, 500)
BG_COLOR = (255, 255, 255)

NODE_R = 4
NODE_COLOR = (0, 0, 255)

EDGE_COLOR = (0, 0, 0)


def __create_baseimage(size, bg_color, nodes, edges):
  img = Image.new('RGB', size, color=bg_color)
  draw = ImageDraw.Draw(img)
  for node in nodes.values():
    draw.ellipse((node.x - NODE_R, node.y - NODE_R, node.x + NODE_R, node.y + NODE_R), fill=NODE_COLOR)
  for edge in edges:
    draw.line((edge.st.as_tuple(), edge.ed.as_tuple()), fill=EDGE_COLOR)
  return img


def draw_graph(filename, nodes, edges):
  img = __create_baseimage(SIZE, BG_COLOR, nodes, edges)
  img.save(filename)