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
from src.input_handler import InputHandler
import pygame

class TestInputHandler(unittest.TestCase):
    def setUp(self):
        # Mock the GameLogic to pass into InputHandler
        self.mock_game_logic = Mock()
        self.input_handler = InputHandler(game_logic=self.mock_game_logic)

    def test_process_input(self):
        """Test that input events are processed correctly."""
        # Mock the pygame event queue
        with patch('pygame.event.get') as mock_get:
            # Create mock events for pygame to return
            mock_event_down = Mock(type=pygame.KEYDOWN, key=pygame.K_LEFT)
            mock_event_up = Mock(type=pygame.KEYUP, key=pygame.K_RIGHT)

            # Set mock_get to return these events
            mock_get.return_value = [mock_event_down, mock_event_up]

            # Process each event
            for event in pygame.event.get():
                self.input_handler.process_event(event)

            # Check if the correct commands are set based on the events
            self.assertTrue('move_left' in self.input_handler.commands, "Left arrow key should trigger move_left command.")
            self.assertFalse('move_right' in self.input_handler.commands, "Right arrow key should not remain active after key up.")

if __name__ == '__main__':
    unittest.main()
