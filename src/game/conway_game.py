from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Game():
    """Class representing a game of conway's game of life.

    Instance attributes:
        - initial_field: The initial field
        - max_width: Maximum field width
        - max_height: Maximum field height
        - field_progression: List of field generations.
        - latest_field: Last field generated.

    Representation Invariants:
        - max_width >= 0
        - max_height >= 0
    """
    initial_field: Field
    max_width: int
    max_height: int
    latest_field: Field = None

    # Private attributes:
    # - _field_progression: List of previous computed field states
    _field_progression: list[Field] = field(default_factory=list)

    @property
    def age(self) -> int:
        """Gets age of game."""
        return len(self._field_progression)

    def run(self, max_generations: int) -> None:
        """Simulates the game"""
        if self.latest_field is None:
            self.latest_field = self.initial_field
        for _ in range(0, max_generations):
            if len(self.latest_field.live_state) == 0:
                exit
            else:
                self.latest_field = self.latest_field.next_generation()
                self._field_progression.append(self.latest_field)


@dataclass
class Cell():
    """Class representing a normal, static cell.

    Instance Attributes:
        - x: X axis location of the cell.
        - y: Y axis location of the cell.

    Representation Invariants:
        - x >= 0
        - y >= 0
    """
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, type(self)):
            return NotImplemented
        return self.x == o.x and self.y == o.y


@dataclass
class Field():
    """"Class representing game field state.

    Instance attributes:
        - width: Maximum cell width of field
        - height: Maximum cell height of field
        - live_state: Set of live cells on field
        - petrified_state: Set of petrified cells on field
    """
    width: int
    height: int
    live_state: set[Cell]
    petrified_state: set[Cell]

    def get_neighbors(self, cell: Cell) -> set[Cell]:
        """Returns neighbors of a live cell if the cell is in field bounds."""
        neighbors = set()

        if cell.x - 1 >= 0:
            neighbors.add(Cell(cell.x - 1, cell.y))
        if cell.x - 1 >= 0 and cell.y - 1 >= 0:
            neighbors.add(Cell(cell.x - 1, cell.y - 1))
        if cell.x - 1 >= 0 and cell.y + 1 < self.height:
            neighbors.add(Cell(cell.x - 1, cell.y + 1))
        if cell.y - 1 >= 0:
            neighbors.add(Cell(cell.x, cell.y - 1))
        if cell.y - 1 >= 0 and cell.x + 1 < self.width:
            neighbors.add(Cell(cell.x + 1, cell.y - 1))
        if cell.y + 1 < self.height:
            neighbors.add(Cell(cell.x, cell.y + 1))
        if cell.x + 1 < self.width:
            neighbors.add(Cell(cell.x + 1, cell.y))
        if cell.y + 1 < self.height and cell.x + 1 < self.width:
            neighbors.add(Cell(cell.x + 1, cell.y + 1))

        return neighbors

    def next_generation(self) -> Field:
        """Returns the next field generation."""
        counter = {}
        new_live_state = self.live_state

        for cell in self.live_state:
            if cell not in counter:
                counter[cell] = 0

            # Count cell neighbors
            neighbors = self.get_neighbors(cell)
            for nb in neighbors:
                if nb not in counter:
                    counter[nb] = 1
                else:
                    counter[nb] += 1

        # Apply rules.
        for spot in counter:
            if counter[spot] < 2 or counter[spot] > 3:
                new_live_state.discard(spot)
            elif counter[spot] == 3:
                if spot not in self.petrified_state:
                    new_live_state.add(spot)

        return Field(self.width, self.height, new_live_state, self.petrified_state)

    def print_field(self) -> None:
        """Prints field state in console."""
        for y in range(0, self.height):
            line = ""
            for x in range(0, self.width):
                if Cell(x, y) in self.live_state:
                    line += "X"
                elif Cell(x, y) in self.petrified_state:
                    line += "Y"
                else:
                    line += "O"
            print(line)


