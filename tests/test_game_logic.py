"""
Copyright (c) 2024 Adam Billekvist

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import unittest
from unittest.mock import Mock, patch
from src.game_logic import GameLogic
from src.tetrimino import Tetrimino

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        """
        Sets up a GameLogic instance before each test function is executed.

        This setup includes:
        - Mocking sound effects to prevent actual audio playback during tests.
        - Replacing the Tetrimino class with a mock to simulate its behavior without real game logic.
        """
        self.mock_rotate_sound = Mock()
        self.mock_break_line_sound = Mock()
        self.game_logic = GameLogic(break_line_sound=self.mock_break_line_sound, rotate_sound=self.mock_rotate_sound)
        self.mock_tetrimino = Mock(spec=Tetrimino)
        self.game_logic.current_tetrimino = self.mock_tetrimino

    def test_initialization(self):
        """
        Tests the initial state of GameLogic upon instantiation.

        Verifies that the game starts with a score of zero, no game over condition, and the game not paused.
        """
        self.assertEqual(self.game_logic.score, 0)
        self.assertFalse(self.game_logic.game_over)
        self.assertFalse(self.game_logic.is_paused, "Game should start in an unpaused state.")

    def test_clear_lines(self):
        """
        Tests the behavior of clearing lines in the game grid.

        This function simulates a full line at the bottom of the grid and triggers the line clearing process.
        It checks that the score is increased and the line clearing sound is played exactly once.
        """
        self.game_logic.grid[-1] = [1] * len(self.game_logic.grid[0])
        self.game_logic.clear_lines()
        self.mock_break_line_sound.play.assert_called_once()
        self.assertGreater(self.game_logic.score, 0, "Score should increase when a line is cleared.")

    def test_toggle_pause(self):
        """
        Tests the toggle functionality of the game's pause state.

        Ensures that calling toggle_pause changes the game's pause status from False to True and vice versa.
        """
        self.assertFalse(self.game_logic.is_paused)
        self.game_logic.toggle_pause()
        self.assertTrue(self.game_logic.is_paused)
        self.game_logic.toggle_pause()
        self.assertFalse(self.game_logic.is_paused, "Toggling pause again should resume the game.")

    def test_reset_game(self):
        """
        Tests the reset functionality of the game to ensure it returns to its initial state.

        After modifying the game state, invoking reset_game should revert all properties to their default values.
        """
        self.game_logic.score = 100
        self.game_logic.game_over = True
        self.game_logic.is_paused = True
        self.game_logic.reset_game()
        self.assertEqual(self.game_logic.score, 0)
        self.assertFalse(self.game_logic.game_over)
        self.assertFalse(self.game_logic.is_paused)

    def test_clear_multiple_lines(self):
        """
        Tests the game's scoring logic when multiple lines are cleared simultaneously.

        Verifies that clearing multiple lines results in an appropriate increase in score according to the game's rules.
        """
        # Setup two consecutive full lines at the bottom of the grid.
        for i in range(-2, 0):
            self.game_logic.grid[i] = [1] * len(self.game_logic.grid[0])
        self.game_logic.clear_lines()
        self.mock_break_line_sound.play.assert_called_once()
        expected_score_increase = 4  # Example score logic: score per line squared (2 lines -> 2^2 = 4)
        self.assertEqual(self.game_logic.score, expected_score_increase, "Score should correctly reflect multiple lines cleared.")

if __name__ == '__main__':
    unittest.main()
