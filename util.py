# Util

from config import *


neighbor_positions = []

for i in range(N):
  p_neighbors = []

  x = i %  SIZE
  y = i // SIZE

  if x > 0: p_neighbors.append(i - 1)
  if x < SIZE - 1: p_neighbors.append(i + 1)
  if y > 0: p_neighbors.append(i - SIZE)
  if y < SIZE - 1: p_neighbors.append(i + SIZE)

  neighbor_positions.append(p_neighbors)


def parse_move(text, size):
  text = text.strip().lower()

  if text == "pass": return None
  x = ord(text[0]) - ord("a")
  y = int(text[1:]) - 1

  if not (0 <= x < size and 0 <= y < size):
    return "invalid"

  return y * size + x