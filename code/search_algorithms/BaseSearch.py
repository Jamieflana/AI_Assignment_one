import time
from maze import N, S, E, W


class BaseSearch:
    """
    Parent class for all algorithms which will include the
    evaluation metrics
    """

    def __init__(self):
        self.reset_metrics()

    def reset_metrics(self):
        self.nodes_expanded: int = 0
        self.nodes_generated: int = 0
        self.max_frontier_size: int = 0
        self.path_length: int = 0
        self.run_time: float = 0
        self.found: bool = False

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
        self.reset_metrics()

        time_start = time.perf_counter()
        path = self._search(maze, start, goal)
        time_end = time.perf_counter()

        self.run_time = (time_end - time_start) * 1000.0
        self.found = path is not None
        self.path_length = (len(path) - 1) if path else 0

        metrics = {
            "found": self.found,
            "path_length": self.path_length,
            "nodes_expanded": self.nodes_expanded,
            "nodes_generated": self.nodes_generated,
            "max_frontier_size": self.max_frontier_size,
            "runtime": self.run_time,
        }
        return path, metrics

    def _search(self, maze, start, goal):
        raise NotImplementedError("Subclasses must implement _search().")
