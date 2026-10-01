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

  if len(text) < 2: return "invalid"

  x = ord(text[0]) - ord("a")
  try: y = int(text[1:])
  except ValueError: return "invalid"

  if not (0 <= x < size and 1 <= y <= size): return "invalid"
  y = size - y

  return y * size + x


def print_board(board):
  letters = [chr(ord("A") + i + (i >= 8)) for i in range(SIZE)]

  print()
  print("   " + " ".join(letters))

  for y in range(SIZE):
    row = []
    for x in range(SIZE):
      position = y * SIZE + x

      if   board[position] == BLACK: stone = "O"
      elif board[position] == WHITE: stone = "X"
      else: stone = "·"
      row.append(stone)

    print(f"{SIZE-y:2} " + " ".join(row) + f" {SIZE-y:2}")

  print("   " + " ".join(letters))
  print()