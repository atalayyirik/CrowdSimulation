"""
This file contains the various elements that can be placed in the grid.

"""
# authors: Leilani Tam von Burg, Atalay Yirik, Michael Hussak

# general imports
import math

# typing imports
from typing import Optional


class Cell:
    def __init__(self, x: int, y: int):
        """

        :param x: x-Coordinate of the Cell
        :param y: y-Coordinate of the Cell
        """
        self.x = x
        self.y = y
        self.name = " "
        self.position = (x, y)

    def right(self) -> 'Cell':
        """
        This function returns the Cell-Object placed to the right of itself
        :return: Cell-Object to the right
        """
        return Cell(self.x, self.y + 1)

    def left(self) -> 'Cell':
        """
        This function returns the Cell-Object placed to the left of itself
        :return: Cell-Object to the left
        """
        return Cell(self.x, self.y - 1)

    def up(self) -> 'Cell':
        """
        This function returns the Cell-Object placed above itself
        :return: Cell-Object above
        """
        return Cell(self.x - 1, self.y)

    def down(self) -> 'Cell':
        """
        This function returns the Cell-Object placed below itself
        :return: Cell-Object below
        """
        return Cell(self.x + 1, self.y)

    def distance(self, other: 'Cell') -> float:
        """
        This function calculates the distance between itself and another given cell
        :param other: Cell, the distance should be calculated to
        :return: calculated distance
        """
        return math.sqrt(((other.x - self.x) ** 2) + ((other.y - self.y) ** 2))

    def is_equal(self, other: 'Cell') -> bool:
        """
        This functions checks, if a given cell has the same position
        :param other: Cell, the position should be checked against
        :return: True if position is equal
        """
        return self.position == other.position


class Pedestrian(Cell):
    def __init__(self, x: int, y: int, name: str = "", speed_meter_per_sec: float = 1.33, age: int = 25):
        """
        Pedestrian-Object, inherits from Cell-Class and represents a Pedestrian-Cell

        :param x: x-Coordinate of the Pedestrian
        :param y: y-Coordinate of the Pedestrian
        :param name: The name of pedestrian
        :param speed_meter_per_sec: The maximum walking speed of the pedestrian
        :param age: The age of the pedestrian
        """
        super().__init__(x, y)
        # This variable represents the dimensions, a pedestrian has
        self.body_dimension = 1 / 3
        self.name = "P" + name
        self.age = age
        # Variable to count the iteration steps to target
        self.steps_to_target = 1
        # Variable to count the movements till target is reached
        self.moved_cells = 1
        self.speed_meter_per_sec = speed_meter_per_sec
        # Variable the final speed in dependence of moved_cells and steps_to_target is calculated
        self.actual_speed = None
        self.measured_speed = None
        self.steps_in_measurement = 0
        self.start_measurement = 0
        self.is_finished = False


class Obstacle(Cell):
    def __init__(self, x: int, y: int):
        """
        Obstacle-Object, inherits from Cell-Class and represents a Obstacle-Cell

        :param x: x-Coordinate of the Obstacle
        :param y: y-Coordinate of the Obstacle
        """
        super().__init__(x, y)
        self.name = "O"


class Target(Cell):
    def __init__(self, x: int, y: int):
        """
        Target-Object, inherits from Cell-Class and represents a Target-Cell

        :param x: x-Coordinate of the Target
        :param y: y-Coordinate of the Target
        """
        super().__init__(x, y)
        self.name = "T"
