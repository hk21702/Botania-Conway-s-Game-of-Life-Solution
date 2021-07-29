from dataclasses import dataclass
from .conway_game import Game, Cell, Field


class BotaniaGame(Game):
    """Botania's modified game of life.

    Instance Attributes:
        - initial_field: The initial field
        - max_width: Maximum field width
        - max_height: Maximum field height
        - field_progression: List of field generations.
        - latest_field: Last field generated.

    Representation Invariants:
        - max_width >= 0
        - max_height >= 0
    """
    max_height: int
    max_width: int
    dandelifeon: Cell
    max_maturity: int
    value_multiplier: int

    # Private Instance Attributes
    # - _collection_cells: Cells on the field that trigger halt
    _collection_cells: set[Cell]

    def __init__(self, initial_field: Field, max_width: int = 25, max_height: int = 25,
                 dandelifeon: Cell = Cell(12, 12), max_maturity: int = 100, value_multiplier: int = 60) -> None:
        initial_field.petrified_state.add(dandelifeon)
        super(BotaniaGame, self).__init__(initial_field, max_width, max_height)

        self.dandelifeon = dandelifeon
        self._collection_cells = self.initial_field.get_neighbors(
            self.dandelifeon)
        self.max_maturity = max_maturity
        self.value_multiplier = value_multiplier

    def run(self, max_generations: int = 200) -> int:
        """Returns theoretical Botania game of life mana score."""
        if self.latest_field is None:
            self.latest_field = self.initial_field

        for _ in range(0, max_generations):
            if len(self.latest_field.live_state) == 0:
                exit
            else:
                self.latest_field = self.latest_field.next_generation()
                self._field_progression.append(self.latest_field)
                halting_cells = self._collection_cells.intersection(
                    self.latest_field.live_state)

                if len(halting_cells) != 0:
                    if self.age < self.max_maturity:
                        score = len(halting_cells) * self.age * \
                            self.value_multiplier
                    else:
                        score = len(halting_cells) * \
                            self.max_maturity * self.value_multiplier
                    return score
        return 0
