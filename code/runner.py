import random

from search_algorithms.BFS import BFS
from maze import Maze
from search_algorithms.DFS import DFS

# Random size between 5x5 and 50x50 (inclusive).
width = random.randint(10, 10)
height = random.randint(10, 10)

# Random loop probability to allow multiple paths.
loop_prob = random.uniform(0.05, 0.30)

# Chance to force an unsolvable maze.
unsolvable_prob = 0.30
solvable = False if random.random() < unsolvable_prob else True

maze = Maze.generate(width, height, loop_prob=loop_prob, solvable=solvable)
start = (0, 0)
goal = (width - 1, height - 1)

print(f"Maze size: {width}x{height} | loop_prob={loop_prob:.2f} | solvable={solvable}")
# print(maze)

DFS_searcher = DFS()
path = DFS_searcher.solve(maze, start, goal)
if path is not None:
    print("Solution found")
else:
    print("Solution not found")

BFS_searcher = BFS()
path = BFS_searcher.solve(maze, start, goal)
if path is not None:
    print("BFS SOlution found")
else:
    print("NO BFS solution found")
