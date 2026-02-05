# code/search_algorithms/DFS.py
from search_algorithms.BaseSearch import BaseSearch


class DFS(BaseSearch):
    def __init__(self):
        super().__init__()

    def neighbors(self, maze, cell):
        return super().neighbors(maze, cell)

    def _search(self, maze, start, goal):
        stack = [start]
        visited = set([(start.x, start.y)])
        parent = {(start.x, start.y): None}

        while stack:
            current = stack.pop()
            self.nodes_expanded += 1

            if current.x == goal.x and current.y == goal.y:
                return self.reconstruct_path(parent, goal)

            for nb in self.neighbors(maze, current):
                key = (nb.x, nb.y)
                if key not in visited:
                    self.nodes_generated += 1
                    visited.add(key)
                    parent[key] = (current.x, current.y)
                    stack.append(nb)
                    if len(stack) > self.max_frontier_size:
                        self.max_frontier_size = len(stack)

        return None

    def solve(self, maze, start, goal):
        """
        Entry Point for the DFS, BFS and A*
        """
        # return self.search(maze, start, goal)
        return super().solve(maze, start, goal)

    def reconstruct_path(self, parent, goal):
        path = []
        cur = (goal.x, goal.y)
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path
