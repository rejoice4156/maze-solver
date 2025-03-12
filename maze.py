from cell import Cell
import random
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        entry_pos_x = 0
        entry_pos_y = 0
        exit_pos_x = self._num_cols - 1
        exit_pos_y = self._num_rows - 1
        entry = self._cells[entry_pos_x][entry_pos_y]
        exit = self._cells[exit_pos_x][exit_pos_y]
        entry.has_top_wall = False
        exit.has_bottom_wall = False
        self._draw_cell(entry_pos_x, entry_pos_y)
        self._draw_cell(exit_pos_x, exit_pos_y)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))

            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))

            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))

            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False

            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False

            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, i, j):
        self._animate()
        current = self._cells[i][j]
        current.visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # left
        if i > 0:
            target = self._cells[i - 1][j]
            if (
                not current.has_left_wall
                and not target.has_right_wall
                and not target.visited
            ):
                current.draw_move(target)
                if self._solve_r(i - 1, j):
                    return True
                current.draw_move(target, undo=True)

        # up
        if j > 0:
            target = self._cells[i][j - 1]
            if (
                not current.has_top_wall
                and not target.has_bottom_wall
                and not target.visited
            ):
                current.draw_move(target)
                if self._solve_r(i, j - 1):
                    return True
                current.draw_move(target, undo=True)

        # right
        if i < self._num_cols - 1:
            target = self._cells[i + 1][j]
            if (
                not current.has_right_wall
                and not target.has_left_wall
                and not target.visited
            ):
                current.draw_move(target)
                if self._solve_r(i + 1, j):
                    return True
                current.draw_move(target, undo=True)

        # down
        if j < self._num_rows - 1:
            target = self._cells[i][j + 1]
            if (
                not current.has_bottom_wall
                and not target.has_top_wall
                and not target.visited
            ):
                current.draw_move(target)
                if self._solve_r(i, j + 1):
                    return True
                current.draw_move(target, undo=True)

        return False

    def solve(self):
        return self._solve_r(0, 0)
