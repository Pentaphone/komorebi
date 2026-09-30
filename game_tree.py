# Game Tree

from gameplay import play, get_legal_moves
from simulation import simulate

import math


class Node:
  def __init__(self,
    board,
    player,
    parent=None,
    move=None,
    position_history=None
  ):
    self.board = board
    self.move = move
    self.player = player

    self.parent = parent
    self.children = []
    self.potential_moves = get_legal_moves(board, player, position_history)
    
    self.visits = 0
    self.wins = 0

  def expand(self):
    if not self.potential_moves: return None

    move = self.potential_moves.pop()
    new_board = self.board.copy()
    position_history = [position.copy() for position in self.position_history]

    if move is not None:
      play(new_board, move, self.player, position_history)

    child = Node(
      new_board,
      self.player,
      parent = self,
      move = move,
      position_history = position_history
    )
    self.children.append(child)
    return child


def mcts(root_node, iterations):
  for _ in range(iterations):
    node = select(root_node)

    if node.potential_moves:
      node = node.expand()

    result = simulate(
      node.board,
      node.player,
      root_node.player
    )
    backpropagate(node, result, root_node.player)

  return root_node


def select(node):
  # find child note with highest upper confidence bound
  while node.children:
    node = max(node.children, key=lambda child: upper_confid_bound(child))

  return node


def upper_confid_bound(node, exploration_const=1.414):
  if node.visits == 0: return float("inf")

  exploitation = node.wins / node.visits
  exploration = (exploration_const * math.sqrt(
    math.log(node.parent.visits) / node.visits
  ))

  return exploitation + exploration


def backpropagate(node, result, player):
  while node:
    node.visits += 1

    if node.player == player:
      node.wins += result
    else:
      node.wins -= result
    
    node = node.parent

  
def choose_move(board, player, position_history, iterations=10_000):
  root = Node(
    board.copy(),
    player,
    position_history=[position.copy() for position in position_history]
  )
  mcts(root, iterations)
  best_node = max(root.children, key=lambda child: child.visits)

  return best_node.move