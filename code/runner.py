from maze import Maze
from search_algorithms.DFS import DFS

width, height = 5, 5

maze = Maze.generate(width, height)
start = maze[0, 0]
goal = maze[width - 1, height - 1]

dfs = DFS()
path, metrics = dfs.solve(maze, start, goal)
print(path)
print(metrics)
