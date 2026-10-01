# Game Tree

from config import *
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

    self.position_history = position_history
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
      player = -self.player,
      parent = self,
      move = move,
      position_history = position_history
    )
    self.children.append(child)
    return child


def mcts(root_node, iterations):
  for i in range(iterations):
    node = select(root_node, root_node.player)

    if node.potential_moves:
      node = node.expand()

    result = simulate(
      node.board,
      node.player
    )
    backpropagate(node, result, root_node.player)

    if i % 100 == 0:
      print(
        f"  Iteration {i:>5}/{iterations:>5}: {root_node.visits:>5} visits, {root_node.wins:>5} wins"
      )
  return root_node


def select(node, root_player):
  # find child note with highest / lowest upper confidence bound
  # depending on which players turn it is
  while not node.potential_moves and node.children:    
    if node.player == root_player:
      node = max(node.children, key=lambda child: upper_confid_bound(child))
    else:
      node = min(node.children, key=lambda child: upper_confid_bound(child))
  return node


def upper_confid_bound(node, exploration_const=EXPLORATION_CONSTANT):
  if node.visits == 0: return float("inf")

  exploitation = node.wins / node.visits
  exploration = (exploration_const * math.sqrt(
    math.log(node.parent.visits) / node.visits
  ))

  return exploitation + exploration


def backpropagate(node, result, root_player):
  while node:
    node.visits += 1

    if result == root_player:
      node.wins += 1
    elif result == -root_player:
      node.wins -= 1
    
    node = node.parent

  
def choose_move(board, player, position_history, iterations=10_000):
  root = Node(
    board.copy(),
    player,
    position_history=[position.copy() for position in position_history]
  )
  mcts(root, iterations)
  print_tree(root, max_depth=4)
  best_node = max(root.children, key=lambda child: child.visits)

  return best_node.move


### Printing
def format_move(move):
  if move is None: return "pass"

  x = move % SIZE
  y = move // SIZE
  return f"{chr(ord('A') + x)}{SIZE - y}"


def print_tree(node, depth=0, max_depth=None):
  indent = "  " * depth

  if node.parent is None: move = "root"
  else: move = format_move(node.move)

  if node.visits: value = node.wins / node.visits
  else: value = 0

  if node.parent is not None: ucb = upper_confid_bound(node)
  else: ucb = 0

  print(
    f"{indent}"
    f"move={move} "
    f"visits={node.visits} "
    f"wins={node.wins:>3} "
    f"value={value:.3f} "
    f"UCT={ucb:.3f}"
  )
  if max_depth is not None and depth >= max_depth:
    return

  for child in sorted(
    node.children,
    key=lambda child: child.visits,
    reverse=True
  ):
    print_tree(child, depth+1, max_depth)