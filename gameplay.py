# Gameplay

### Imports
from config import *
from util import neighbor_positions

import numpy as np


### gameplay components
def play(board, position, player, position_history, record=True):
  if board[position] != EMPTY: return False
  old_board = board.copy()

  board[position] = player

  # Capture
  opponent = -player
  for neighbor in neighbor_positions[position]:
    if board[neighbor] != opponent: continue
    opponent_group = get_group(board, neighbor)
    if not get_liberties(board, opponent_group):
      remove_group(board, opponent_group)

  if not ALLOW_SELF_CAPTURE:
    if not get_liberties(board, get_group(board, position)):
        board[:] = old_board
        return False

  # simple ko rule
  if len(position_history) > 0:
    if np.array_equal(board, position_history[-1]):
      board[:] = old_board
      return False

  if record: position_history.append(board.copy())
  return True


def get_group(board, start):
  color = board[start]
  group = {start}
  stack = [start]

  while stack:
    position = stack.pop()
    for neighbor in neighbor_positions[position]:
      if (
        board[neighbor] == color
        and neighbor not in group
      ):
        group.add(neighbor)
        stack.append(neighbor)

  return group


def remove_group(board, group):
  for position in group:
    board[position] = EMPTY


def get_liberties(board, group):
  liberties = set()
  for position in group:
    for neighbor in neighbor_positions[position]:
      if board[neighbor] == EMPTY:
        liberties.add(neighbor)

  return liberties


def get_legal_moves(board, player, position_history):
  moves = []

  for position in range(len(board)):
    if board[position] != EMPTY: continue

    test_board = board.copy()
    if play(test_board, position, player, position_history, record=False):
      moves.append(position)

  return moves


### Scoring
def get_territory(board, start):
  territory = set()
  borders = set()
  stack = [start]

  while stack:
    position = stack.pop()

    if position in territory: continue

    if board[position] != EMPTY: continue

    territory.add(position)
    for neighbor in neighbor_positions[position]:
      if board[neighbor] == EMPTY:
        stack.append(neighbor)
      else:
        borders.add(board[neighbor])

  if len(borders) == 1:
    return territory, borders.pop()

  # Dame / neutral territory
  return territory, None


def calculate_result(board):
  black_score = np.count_nonzero(board == BLACK)
  white_score = np.count_nonzero(board == WHITE)

  visited = set()

  for position in range(len(board)):
    if board[position] != EMPTY: continue
    if position in visited: continue

    territory, owner = get_territory(board, position)
    visited.update(territory)

    if owner == BLACK:
      black_score += len(territory)

    elif owner == WHITE:
      white_score += len(territory)

  if black_score > white_score:
      return BLACK

  if white_score > black_score:
      return WHITE

  return 0
