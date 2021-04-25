"""
This file contains the Simulation Model

"""
# authors: Leilani Tam von Burg, Atalay Yirik, Michael Hussak

# relative imports
from Elements import Cell, Pedestrian, Obstacle, Target


class Model:
    def __init__(
            self,
            grid_width: int,
            grid_height: int,
            grid_unit: int = 10,
            pedestrians: list = [],
            targets: list = [],
            obstacles: list = [],
            in_meter: bool = False,
            disappear: bool = True
    ):
        """

        :param grid_width: width of the grid
        :param grid_height: height of the grid
        :param grid_unit: pixels of one grid
        :param pedestrians: list of pedestrians to be added to grid initially
        :param targets: list of targets to be added to grid initially
        :param obstacles: list of obstacles to be added to grid initially
        :param in_meter: if True, grid is resized to meter (depending on body_dimension) instead of cell quantity
        :param disappear: if True, pedestrians disappear in the target
        """
        self.grid_unit = grid_unit
        self.body_dimension = 1 / 3
        self.grid_width = grid_width
        self.grid_height = grid_height
        # changing grid dimensions in case the scale is in meter, otherwise scale is in cell quantity
        if in_meter:
            self.grid_width = grid_width * int(1 / self.body_dimension)  
            self.grid_height = grid_height * int(1 / self.body_dimension)
        self.empty = " " 
        self.obstacles = obstacles
        self.pedestrians = pedestrians
        self.targets = targets
        self.grid = self.create_empty_grid()
        # function call must be before self.placeStates()
        self.set_pedestrian_names()
        # placing the various states in the grid
        self.place_states()
        self.disappear = disappear

    def set_pedestrian_names(self):
        """
        This function renames the pedestrian and gives them a unique name
        :return: None
        """
        for idx, p in enumerate(self.pedestrians):
            p.name += str(idx)

    def create_empty_grid(self) -> list:
        """
        This function creates an empty grid
        :return: list of lists
        """
        return [[self.empty] * self.grid_width for _ in range(self.grid_height)]

    def place_states(self):
        """
        This function is used initially and places pedestrians, obstacles and targets in the grid
        :return: None
        """
        for cell in self.pedestrians + self.obstacles + self.targets:
            self.grid[cell.x][cell.y] = cell.name

    def all_finished(self) -> bool:
        """
        This function checks, if all pedestrians have reached the target
        :return: False, if at least one pedestrian did not reach the target
        """
        for p in self.pedestrians:
            if not p.is_finished:
                return False
        return True

    # Todo: is that function necessary?
    def simulate(self):
        """

        :return:
        """
        while not self.all_finished():
            self.simulate_one_step()

    def update(self, p: Pedestrian, shortest_cell: Cell):
        """
        This function updates the variables of a given pedestrian according to the cell with shortest distance to
        the target. shortest_cell might be equal to p in case there is no free cell closer to target.

        :param p: Pedestrian to be updated
        :param shortest_cell: cell, the pedestrian is updated to
        :return: None
        """
        self.grid[p.x][p.y] = self.empty
        self.grid[shortest_cell.x][shortest_cell.y] = p.name
        p.x = shortest_cell.x
        p.y = shortest_cell.y
        p.position = (p.x, p.y)
        """
        if self.pedestrians[i].x==49*3 and 4*3 < self.pedestrians[i].y <= 6 *3:
            self.pedestrians[i].start_measurement = self.pedestrians[i].steps_to_target 
        if self.pedestrians[i].x==51*3 and 4*3 < self.pedestrians[i].y <= 6 *3:
            # calculating steps in measurement station 
            self.pedestrians[i].steps_in_measurement = (
            self.pedestrians[i].start_measurement - self.pedestrians[i].steps_to_target)
            # calculate measured speed 
            self.pedestrians[i].measured_speed = (
            2*3/self.pedestrians[i].steps_in_measurement)*self.pedestrians[i].speed_meter_per_sec
        """

    def simulate_one_step(self):
        """
        This functions simulates one step of all available pedestrians
        :return: None
        """
        # variable used to check, if in this iteration one pedestrian reached the target
        ped_in_target = False

        for p in self.pedestrians:
            if not p.is_finished:
                p.steps_to_target += 1
                # finding cell closest to target
                shortest_cell = self.find_shortest_move(p)
                # in case next step is into the target cell
                if not ped_in_target and shortest_cell in self.targets:
                    p.is_finished = True
                    p.moved_cells += 1
                    # calculating the actual speed depending on the moved_cells and the steps_to_target
                    p.actual_speed = (p.moved_cells / p.steps_to_target) * p.speed_meter_per_sec
                    # freeing the cell
                    if self.disappear:
                        self.grid[p.x][p.y] = self.empty
                    ped_in_target = True
                elif shortest_cell not in self.targets:
                    position_before = p.position
                    self.update(p, shortest_cell)
                    # counting position moves, might not change in case shortest_cell == p
                    if not p.position == position_before:
                        p.moved_cells += 1

    def is_valid(self, c: Cell) -> bool:
        """
        Checking if a given Cell is available

        :param c: Cell to be checked if it is available
        :return: True if cell available and in dimensions of grid
        """
        return 0 <= c.x < self.grid_height and 0 <= c.y < self.grid_width and self.grid[c.x][c.y] == self.empty

    def find_shortest_move(self, p: Pedestrian) -> Cell:
        """
        This function looks for the cell that is closest to the target and is available.
        In case no closer cell is free, it returns itself.

        :param p: Pedestrian, the best move should be found for
        :return: Returns either an empty Cell or the Pedestrian itself
        """
        current_distance = p.distance(self.targets[0])
        shortest_cell = p
        # possible moves
        moves = [p.left, p.right, p.up, p.down]
        for target in self.targets:
            for move in moves:
                # in case the move is to the target
                if move().is_equal(target):
                    shortest_cell = target
                # in case the move is valid and leads to a state closer to the target
                elif self.is_valid(move()) and move().distance(target) < current_distance:
                    current_distance = move().distance(target)
                    shortest_cell = move()
        return shortest_cell
