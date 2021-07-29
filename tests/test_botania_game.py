import pytest

from game import BotaniaGame
from game import Field, Cell


class TestDefaultOptimalBotaniaGame:
    live_cells = {Cell(11, 2), Cell(12, 2), Cell(
        13, 2), Cell(12, 3), Cell(15, 3), Cell(15, 4)}
    petrified_cells = {Cell(17, 1), Cell(17, 4), Cell(9, 5), Cell(
        15, 5), Cell(7, 10), Cell(12, 10), Cell(17, 10)}
    field = Field(25, 25, live_cells, petrified_cells)

    def test_optimal_score_default(self):
        """"Asserts that an optimal setup with default settings results in 36000 score."""
        game = BotaniaGame(self.field)
        assert game.run() == 36000

    def test_optimal_score_default(self):
        """"Asserts that an optimal setup with default halts at 100 generations."""
        game = BotaniaGame(self.field)
        game.run()
        assert game.age == 100
