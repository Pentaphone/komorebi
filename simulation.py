# Simulation

### Imports
from config import *
from gameplay import play, get_legal_moves, calculate_result
from util import print_board

import random

def simulate(board, player, moves_limit=MOVES_LIMIT):
  board = board.copy()
  position_history = [board.copy()]
  passes = 0

  for _ in range(moves_limit):
    legal_moves = get_legal_moves(board, player, position_history)

    if legal_moves:
      move = random.choice(legal_moves)
      if random.random() < PASS_PROBABILITY:
        passes += 1
        if passes >= 2: break
      else:
        if play(board, move, player, position_history): passes = 0

    else:
      passes += 1
      if passes >= 2: break
    
    player = -player

  return calculate_result(board)