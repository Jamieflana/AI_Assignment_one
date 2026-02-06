from search_algorithms.BaseSearch import BaseSearch
from collections import deque


class BFS(BaseSearch):
    def __init__(self):
        super().__init__()

    def _search(self, maze, start, goal):
        start_cell = maze[start]
        goal_cell = maze[goal]

        if start_cell is None or goal_cell is None:
            return None

        queue = deque([start_cell])
        visited = {(start_cell.x, start_cell.y)}
        parent = {(start_cell.x, start_cell.y): None}

        while queue:
            cell = queue.popleft()
            if (cell.x, cell.y) == (goal_cell.x, goal_cell.y):
                path = []
                cur = (cell.x, cell.y)
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                path.reverse()
                return path
            for neighbor in self.neighbors(maze, cell):
                key = (neighbor.x, neighbor.y)
                if key not in visited:
                    visited.add(key)
                    parent[key] = (cell.x, cell.y)
                    queue.append(neighbor)
        return None
