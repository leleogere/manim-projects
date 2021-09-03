from manim import *

def make_step(state):
    def count_neighbours(grid, i, j):
        return np.sum(grid[i - 1:i + 2, j - 1:j + 2]) - grid[i, j]
    new_state = state.copy()
    for i in range(1, state.shape[0] - 1):
        for j in range(1, state.shape[1] - 1):
            neigh = count_neighbours(state, i, j)
            if state[i, j]:
                new_state[i, j] = (neigh == 2 or neigh == 3)
            else:
                new_state[i, j] = (neigh == 3)
    return new_state

def draw_grid(grid, scale=.5):
    cells = VGroup()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j]:
                cell = Square(1).set_fill(opacity=.5).move_to([i, j, 0], aligned_edge=DL).scale(scale, about_point=ORIGIN)
                cells.add(cell)
    return cells

class Conway(Scene):
    grid = np.zeros((30, 30), dtype=bool)
    # first spaceship
    grid[4, 3] = 1
    grid[4, 4] = 1
    grid[4, 5] = 1
    grid[3, 5] = 1
    grid[2, 4] = 1
    # second spaceship
    spaceship2 = np.fliplr(np.array([[0, 1, 1, 0, 0],
                           [1, 1, 1, 1, 0],
                           [1, 1, 0, 1, 1],
                           [0, 0, 1, 1, 0]])).transpose()
    coords2 = [19, 9]
    grid[coords2[0]:coords2[0]+spaceship2.shape[0], coords2[1]:coords2[1]+spaceship2.shape[1]] = spaceship2

    state = draw_grid(grid)

    T = 50

    def construct(self):
        self.camera.next_to(ORIGIN, aligned_edge=DL).shift(10*OUT)
        self.add(self.state)
        for t in range(self.T):
            self.wait(.6*(1-t/self.T))
            self.grid = make_step(self.grid)
            temp = self.state
            self.state = draw_grid(self.grid)
            self.play(FadeOut(temp), FadeIn(self.state), run_time=.2)
