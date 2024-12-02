import math
from copy import deepcopy


class Position:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def copy(self):
        """Generate a deep copy of the position and return it."""

        return deepcopy(self)

    def get_coordinates(self):
        return (self.x, self.y, self.z)

    def set_coordinates(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def euclidean_distance(self, other: 'Position'):
        """Calculate the Euclidean distance between this position and another and return it.

        Parameters
        ----------
        other : Position
            The other position to calculate the distance to.

        Returns
        -------
        float
            The Euclidean distance between the two positions.

        Raises
        ------
        ValueError
            If the other position is not an instance of Position.
        """

        if not isinstance(other, Position):
            raise ValueError("The argument must be an instance of Position")

        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"


if __name__ == "__main__":
    # Example usage
    p1 = Position(1, 2, 3)
    p2 = Position(4, 5, 6)

    print("Position 1:", p1)
    print("Position 2:", p2)

    # Copy a position
    p3 = p1.copy()
    print("Copy of Position 1:", p3)

    # Get coordinates
    print("Coordinates of Position 1:", p1.get_coordinates())

    # Set coordinates
    p3.set_coordinates(7, 8, 9)
    print("New coordinates of Position 3:", p3)

    # Compare positions
    print("Position 1 equals Position 2?", p1 == p2)
    print("Position 1 equals Position 3?", p1 == p3)
    print("Position 1 equals Position 1?", p1 == p1)

    # Calculate Euclidean distance
    distance = p1.euclidean_distance(p2)
    print(
        f"Euclidean distance between Position 1 and Position 2: {distance:.2f}")
