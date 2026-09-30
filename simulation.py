# Simulation

### Imports
from gameplay import play, get_legal_moves, calculate_result

import random

def simulate(board, player):
  board = board.copy()
  position_history = [board.copy()]
  passes = 0

  while True:
    legal_moves = get_legal_moves(board, player, position_history)

    if not legal_moves:
      passes += 1
      if passes >= 2: break
      player = -player
      continue

    move = random.choice(legal_moves)

    if move is None:
      passes += 1
      if passes >= 2: break
      player = -player
      continue

    if play(board, move, player, position_history):
      passes = 0
      player = -player

  return calculate_result(board)