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
from src.tetrimino import Tetrimino

class TestTetrimino(unittest.TestCase):
    def setUp(self):
        """
        Set up conditions for each test case.

        This method prepares a Tetrimino instance and a mock grid which simulates
        the game's playing field. A mock for the rotation sound effect is also created
        to verify interaction with the sound system during rotation.
        """
        # Prepare a 10x20 grid of zeros representing an empty Tetris field.
        self.grid = [[0]*10 for _ in range(20)]
        
        # Initialize a Tetrimino with shape 'I' (a straight line) in the grid.
        self.tetrimino = Tetrimino('I', self.grid)
        
        # Create a mock object to simulate the sound played during rotation.
        self.mock_rotate_sound = Mock()

    def test_rotate_successful(self):
        """
        Test successful rotation of a Tetrimino.

        Verifies that the Tetrimino's rotation attribute updates correctly when
        the rotation is successful, i.e., sufficient time has passed according to
        the rotation delay and the rotation does not result in a collision.
        """
        current_time = 1000
        last_rotation_time = 800  # earlier than current_time - rotation_delay
        rotation_delay = 150
        
        # Store initial rotation state to compare after attempting rotation.
        initial_rotation = self.tetrimino.rotation
        
        # Simulate passage of time using a mock for pygame's time function.
        with patch('pygame.time.get_ticks', return_value=current_time):
            result_time = self.tetrimino.rotate(current_time, last_rotation_time, rotation_delay, self.mock_rotate_sound)
        
        # Check that rotation time is updated to current time on success.
        self.assertEqual(result_time, current_time, "Rotation time should update on successful rotation.")
        # Ensure the Tetrimino's rotation state has changed.
        self.assertNotEqual(self.tetrimino.rotation, initial_rotation, "Tetrimino rotation should change.")
        # Verify that the rotation sound was played once.
        self.mock_rotate_sound.play.assert_called_once()

    def test_rotate_unsuccessful(self):
        """
        Test unsuccessful rotation due to insufficient time passed.

        Ensures that the Tetrimino's rotation does not update when not enough time
        has passed since the last rotation, simulating a rapid attempt to rotate that
        is below the allowed rotation speed threshold.
        """
        current_time = 900
        last_rotation_time = 800
        rotation_delay = 150
        
        # Store initial rotation state to confirm no change on failed rotation.
        initial_rotation = self.tetrimino.rotation
        
        # Simulate passage of time for the test.
        with patch('pygame.time.get_ticks', return_value=current_time):
            result_time = self.tetrimino.rotate(current_time, last_rotation_time, rotation_delay, self.mock_rotate_sound)
        
        # Ensure the rotation time remains unchanged on failed rotation attempt.
        self.assertEqual(result_time, last_rotation_time, "Rotation time should not update on failed rotation.")
        # Confirm no change in the Tetrimino's rotation state.
        self.assertEqual(self.tetrimino.rotation, initial_rotation, "Tetrimino rotation should not change.")
        # Ensure the rotation sound was not played.
        self.mock_rotate_sound.play.assert_not_called()

if __name__ == '__main__':
    unittest.main()
