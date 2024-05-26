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
from unittest.mock import Mock, patch, ANY
import pygame
from src.display import Display
import src.settings as settings

class TestDisplay(unittest.TestCase):
    def setUp(self):
        """Prepare environment for testing Display methods.

        Sets up a mocked Pygame environment, particularly focusing on elements like
        screen size and font rendering, which are crucial for Display functionality but
        impractical in a headless test environment.
        """
        pygame.init()
        self.addCleanup(pygame.quit)
        self.mock_screen = Mock()
        self.mock_screen.get_width.return_value = 800
        self.mock_screen.get_height.return_value = 600

        self.mock_font = Mock()
        self.mock_text_surface = Mock()
        self.mock_font.render = Mock(return_value=self.mock_text_surface)

        with patch('pygame.font.Font', return_value=self.mock_font):
            self.display = Display(self.mock_screen)

    def test_init(self):
        """Test initialization of the Display class.

        Ensures that upon initialization, the Display object is configured with
        the correct screen and settings as provided during its creation.
        """
        self.assertEqual(self.display.cell_size, settings.CELL_SIZE)
        self.assertIs(self.display.screen, self.mock_screen)

    def test_render(self):
        """Test the render method of Display.

        This method should correctly invoke drawing functions for the grid,
        tetrimino, and score/level texts based on the game state provided.
        """
        mock_grid = [[0]*10 for _ in range(20)]
        mock_tetrimino = Mock()
        mock_tetrimino.get_current_shape.return_value = [[1]]
        mock_tetrimino.position = [5, 5]

        with patch('pygame.draw.rect'), patch('pygame.Rect'):
            self.display.render(mock_grid, 100, mock_tetrimino, 2, False)
        calls = [
            unittest.mock.call("Score: 100", True, settings.WHITE),
            unittest.mock.call("Level: 2", True, settings.WHITE)
        ]
        self.mock_font.render.assert_has_calls(calls, any_order=True)

    def test_show_paused(self):
        """Test the display of the 'Paused' text during game pause.

        Validates that the paused text is rendered centrally on the screen.
        """
        self.display.show_paused()
        self.mock_screen.blit.assert_called_with(self.mock_text_surface, ANY)

    def test_show_game_over(self):
        """Test the display of the 'Game Over!' text when the game ends.

        Ensures that the game over text is displayed centrally and that the screen is
        updated appropriately.
        """
        with patch('pygame.display.flip'), patch('pygame.time.wait'):
            self.display.show_game_over()
        self.mock_screen.blit.assert_called_with(self.mock_text_surface, ANY)

if __name__ == '__main__':
    unittest.main()