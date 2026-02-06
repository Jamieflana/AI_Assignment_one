from maze import N, S, E, W


class BaseSearch:
    """
    Parent class for search algorithms.
    """

    def __init__(self):
        pass

    def neighbors(self, maze, cell):
        x, y = cell.x, cell.y
        result = []
        if N not in cell.walls:
            result.append(maze[x, y - 1])
        if S not in cell.walls:
            result.append(maze[x, y + 1])
        if W not in cell.walls:
            result.append(maze[x - 1, y])
        if E not in cell.walls:
            result.append(maze[x + 1, y])
        return [c for c in result if c is not None]

    def solve(self, maze, start, goal):
        return self._search(maze, start, goal)

    def _search(self, maze, start, goal):
        raise NotImplementedError("Subclasses must implement _search().")
