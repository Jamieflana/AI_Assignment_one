# -*- coding: utf-8 -*-
import random

# Easy to read representation for each cardinal direction.
N, S, W, E = ("n", "s", "w", "e")


class Cell(object):
    """
    Class for each individual cell. Knows only its position and which walls are
    still standing.
    """

    def __init__(self, x, y, walls):
        self.x = x
        self.y = y
        self.walls = set(walls)

    def __repr__(self):
        # <15, 25 (es  )>
        return "<{}, {} ({:4})>".format(self.x, self.y, "".join(sorted(self.walls)))

    def __contains__(self, item):
        # N in cell
        return item in self.walls

    def is_full(self):
        """
        Returns True if all walls are still standing.
        """
        return len(self.walls) == 4

    def _wall_to(self, other):
        """
        Returns the direction to the given cell from the current one.
        Must be one cell away only.
        """
        assert abs(self.x - other.x) + abs(self.y - other.y) == 1, "{}, {}".format(
            self, other
        )
        if other.y < self.y:
            return N
        elif other.y > self.y:
            return S
        elif other.x < self.x:
            return W
        elif other.x > self.x:
            return E
        else:
            assert False

    def connect(self, other):
        """
        Removes the wall between two adjacent cells.
        """
        other.walls.remove(other._wall_to(self))
        self.walls.remove(self._wall_to(other))


class Maze(object):
    """
    Maze class containing full board and maze generation algorithms.
    """

    # Unicode character for a wall with other walls in the given directions.
    UNICODE_BY_CONNECTIONS = {
        "ensw": "┼",
        "ens": "├",
        "enw": "┴",
        "esw": "┬",
        "es": "┌",
        "en": "└",
        "ew": "─",
        "e": "╶",
        "nsw": "┤",
        "ns": "│",
        "nw": "┘",
        "sw": "┐",
        "s": "╷",
        "n": "╵",
        "w": "╴",
    }

    def __init__(self, width=20, height=10):
        """
        Creates a new maze with the given sizes, with all walls standing.
        """
        self.width = width
        self.height = height
        self.cells = []
        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(Cell(x, y, [N, S, E, W]))

    def __getitem__(self, index):
        """
        Returns the cell at index = (x, y).
        """
        x, y = index
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x + y * self.width]
        else:
            return None

    def neighbors(self, cell):
        """
        Returns the list of neighboring cells, not counting diagonals. Cells on
        borders or corners may have less than 4 neighbors.
        """
        x = cell.x
        y = cell.y
        for new_x, new_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            neighbor = self[new_x, new_y]
            if neighbor is not None:
                yield neighbor

    def _to_str_matrix(self):
        """
        Returns a matrix with a pretty printed visual representation of this
        maze. Example 5x5:

        OOOOOOOOOOO
        O       O O
        OOO OOO O O
        O O   O   O
        O OOO OOO O
        O   O O   O
        OOO O O OOO
        O   O O O O
        O OOO O O O
        O     O   O
        OOOOOOOOOOO
        """
        str_matrix = [["O"] * (self.width * 2 + 1) for i in range(self.height * 2 + 1)]

        for cell in self.cells:
            x = cell.x * 2 + 1
            y = cell.y * 2 + 1
            str_matrix[y][x] = " "
            if N not in cell and cell.y > 0:
                str_matrix[y - 1][x + 0] = " "
            if W not in cell and cell.x > 0:
                str_matrix[y][x - 1] = " "

        return str_matrix

    def __repr__(self):
        """
        Returns an Unicode representation of the maze. Size is doubled
        horizontally to avoid a stretched look. Example 5x5:

        ┌───┬───────┬───────┐
        │   │       │       │
        │   │   ╷   ╵   ╷   │
        │   │   │       │   │
        │   │   └───┬───┘   │
        │   │       │       │
        │   └───────┤   ┌───┤
        │           │   │   │
        │   ╷   ╶───┘   ╵   │
        │   │               │
        └───┴───────────────┘
        """
        # Starts with regular representation. Looks stretched because chars are
        # twice as high as they are wide (look at docs example in
        # `Maze._to_str_matrix`).
        skinny_matrix = self._to_str_matrix()

        # Simply duplicate each character in each line.
        double_wide_matrix = []
        for line in skinny_matrix:
            double_wide_matrix.append([])
            for char in line:
                double_wide_matrix[-1].append(char)
                double_wide_matrix[-1].append(char)

        # The last two chars of each line are walls, and we will need only one.
        # So we remove the last char of each line.
        matrix = [line[:-1] for line in double_wide_matrix]

        def g(x, y):
            """
            Returns True if there is a wall at (x, y). Values outside the valid
            range always return false.

            This is a temporary helper function.
            """
            if 0 <= x < len(matrix[0]) and 0 <= y < len(matrix):
                return matrix[y][x] != " "
            else:
                return False

        # Fix double wide walls, finally giving the impression of a symmetric
        # maze.
        for y, line in enumerate(matrix):
            for x, char in enumerate(line):
                if not g(x, y) and g(x - 1, y):
                    matrix[y][x - 1] = " "

        # Right now the maze has the correct aspect ratio, but is still using
        # 'O' to represent walls.

        # Finally we replace the walls with Unicode characters depending on
        # their context.
        for y, line in enumerate(matrix):
            for x, char in enumerate(line):
                if not g(x, y):
                    continue

                connections = set((N, S, E, W))
                if not g(x, y + 1):
                    connections.remove(S)
                if not g(x, y - 1):
                    connections.remove(N)
                if not g(x + 1, y):
                    connections.remove(E)
                if not g(x - 1, y):
                    connections.remove(W)

                str_connections = "".join(sorted(connections))
                # Note we are changing the matrix we are reading. We need to be
                # careful as to not break the `g` function implementation.
                # If an isolated wall occurs (no adjacent wall connections),
                # fall back to a simple wall character.
                if str_connections:
                    matrix[y][x] = Maze.UNICODE_BY_CONNECTIONS[str_connections]
                else:
                    matrix[y][x] = "│"

        # Simple double join to transform list of lists into string.
        return "\n".join("".join(line) for line in matrix) + "\n"

    def randomize(self, rng=None):
        """
        Knocks down random walls to build a random perfect maze.

        Algorithm from http://mazeworks.com/mazegen/mazetut/index.htm
        """
        rand = rng if rng is not None else random
        cell_stack = []
        cell = rand.choice(self.cells)
        n_visited_cells = 1

        while n_visited_cells < len(self.cells):
            neighbors = [c for c in self.neighbors(cell) if c.is_full()]
            if len(neighbors):
                neighbor = rand.choice(neighbors)
                cell.connect(neighbor)
                cell_stack.append(cell)
                cell = neighbor
                n_visited_cells += 1
            else:
                cell = cell_stack.pop()

    def add_loops(self, loop_prob=0.05, rng=None):
        """
        Adds extra openings to a perfect maze to create loops (imperfect maze).

        loop_prob controls the probability of removing a wall between two
        adjacent cells. Uses only E/S neighbors to avoid double-processing.
        """
        if loop_prob <= 0:
            return

        rand = rng if rng is not None else random
        for cell in self.cells:
            for neighbor in self.neighbors(cell):
                # Only consider east/south to avoid processing each wall twice.
                if neighbor.x < cell.x or neighbor.y < cell.y:
                    continue

                wall_dir = cell._wall_to(neighbor)
                if wall_dir in cell.walls and rand.random() < loop_prob:
                    cell.connect(neighbor)

    @staticmethod
    def generate(
        width=20,
        height=10,
        loop_prob=0.05,
        solvable=True,
        start=(0, 0),
        goal=None,
        max_block_attempts=200,
        rng=None,
    ):
        """
        Returns a new random maze with the given sizes.
        loop_prob > 0 will create loops by removing extra walls.

        solvable:
            True  -> ensure a path exists between start and goal.
            False -> try to remove any path between start and goal.
            None  -> do not enforce either way.
        """
        if goal is None:
            goal = (width - 1, height - 1)
        m = Maze(width, height)
        m.randomize(rng=rng)
        m.add_loops(loop_prob=loop_prob, rng=rng)
        if solvable is False:
            m.block_path(start, goal, max_attempts=max_block_attempts, rng=rng)
        elif solvable is True:
            # Perfect mazes are already solvable; this is a safety check in case
            # any later changes add walls.
            if not m.path_exists(start, goal):
                m.randomize(rng=rng)
                m.add_loops(loop_prob=loop_prob, rng=rng)
        return m

    @staticmethod
    def generate_many(
        sizes, loop_prob=0.05, solvable=True, start=(0, 0), goal=None, rng=None
    ):
        """
        Returns a list of mazes for the given (width, height) sizes.
        """
        mazes = []
        for width, height in sizes:
            mazes.append(
                Maze.generate(
                    width=width,
                    height=height,
                    loop_prob=loop_prob,
                    solvable=solvable,
                    start=start,
                    goal=goal,
                    rng=rng,
                )
            )
        return mazes

    def neighbors_open(self, cell):
        """
        Returns neighbors that are reachable (no wall between).
        """
        for neighbor in self.neighbors(cell):
            if cell._wall_to(neighbor) not in cell.walls:
                yield neighbor

    def _coerce_cell(self, pos):
        if isinstance(pos, Cell):
            return pos
        if pos is None:
            return None
        x, y = pos
        return self[x, y]

    def path_exists(self, start, goal):
        """
        Returns True if there is a path between start and goal.
        """
        start_cell = self._coerce_cell(start)
        goal_cell = self._coerce_cell(goal)
        if start_cell is None or goal_cell is None:
            return False
        if start_cell == goal_cell:
            return True

        queue = [start_cell]
        visited = set([(start_cell.x, start_cell.y)])
        while queue:
            cell = queue.pop(0)
            if cell.x == goal_cell.x and cell.y == goal_cell.y:
                return True
            for nb in self.neighbors_open(cell):
                key = (nb.x, nb.y)
                if key not in visited:
                    visited.add(key)
                    queue.append(nb)
        return False

    def find_path(self, start, goal):
        """
        Returns one path between start and goal as a list of cells, or None.
        """
        start_cell = self._coerce_cell(start)
        goal_cell = self._coerce_cell(goal)
        if start_cell is None or goal_cell is None:
            return None
        if start_cell == goal_cell:
            return [start_cell]

        queue = [start_cell]
        parent = {(start_cell.x, start_cell.y): None}
        visited = set([(start_cell.x, start_cell.y)])

        while queue:
            cell = queue.pop(0)
            if cell.x == goal_cell.x and cell.y == goal_cell.y:
                break
            for nb in self.neighbors_open(cell):
                key = (nb.x, nb.y)
                if key not in visited:
                    visited.add(key)
                    parent[key] = (cell.x, cell.y)
                    queue.append(nb)
        else:
            return None

        path = []
        cur = (goal_cell.x, goal_cell.y)
        while cur is not None:
            cell = self[cur]
            path.append(cell)
            cur = parent[cur]
        path.reverse()
        return path

    def add_wall(self, cell, neighbor):
        """
        Adds a wall between two adjacent cells.
        """
        wall_dir = cell._wall_to(neighbor)
        cell.walls.add(wall_dir)
        neighbor.walls.add(neighbor._wall_to(cell))

    def block_path(self, start, goal, max_attempts=200, rng=None):
        """
        Tries to remove all paths between start and goal by adding walls.
        Returns True if no path remains.
        """
        rand = rng if rng is not None else random
        for _ in range(max_attempts):
            path = self.find_path(start, goal)
            if not path:
                return True
            if len(path) < 2:
                return False

            idx = rand.randrange(len(path) - 1)
            cell = path[idx]
            neighbor = path[idx + 1]
            self.add_wall(cell, neighbor)

        return not self.path_exists(start, goal)
