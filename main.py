# Komorebi

from config import *
from util import parse_move
from game_tree import choose_move
from gameplay import play, calculate_result

import numpy as np

def test():
  print("Hi")

def play_game():
  board = np.zeros(N, dtype=np.int8)
  position_history = [board.copy()]
  player = BLACK
  passes = 0

  while True:
    if player == BLACK:
      move = parse_move(input("Your move: "), SIZE)
      if move == "invalid":
        print("Invalid coordinates")
        continue
      if move == "pass": move = None
      else: move = int(move)

    else:
      print("KomorebiBot is thinking...")
      move = choose_move(
        board,
        player,
        position_history,
        iterations=10_000
      )
      print("KomorebiBot:", move)

    # pass
    if move is None:
      passes += 1
      if passes >= 2: break

    else:
      success = play(board, move, player, position_history)
      if not success:
        print("Illegal move")
        continue
      passes = 0

    player = -player

  result = calculate_result(board)
  if   result == BLACK: print("Black wins")
  elif result == WHITE: print("White wins")
  else: print("Draw")