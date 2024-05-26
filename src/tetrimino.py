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

from . import settings

class Tetrimino:
    """Represents a Tetris piece, capable of rotating and checking its fit within the game grid.

    Attributes:
        shape (str): Identifier for the Tetrimino shape.
        rotation (int): Current rotation index of the Tetrimino.
        grid (list of list of int): The game grid in which the Tetrimino is placed.
        position (list of int): The starting position [row, column] of the Tetrimino on the grid.
        rotate_sound (pygame.mixer.Sound): Sound to play when the Tetrimino rotates.
        rotations (list): A list of rotations where each rotation is defined by a matrix of block positions.
        color (tuple): RGB color value for the Tetrimino.
    """
    def __init__(self, shape, grid, rotate_sound=None):
        """
        Initializes a new instance of a Tetrimino.

        Args:
            shape (str): The shape identifier for the Tetrimino.
            grid (list of list of int): Reference to the game's grid.
            rotate_sound (pygame.mixer.Sound, optional): Sound effect for rotation.
        """
        self.shape = shape
        self.rotation = 0
        self.grid = grid
        self.position = [0, 4]
        self.rotate_sound = rotate_sound
        self.rotations = settings.TETRIMINOS[self.shape]['rotations']
        self.color = settings.TETRIMINOS[self.shape]['color']

    def rotate(self, current_time, last_rotation_time, rotation_delay, rotate_sound):
        """
        Rotate the Tetrimino if the rotation delay has been met.

        Args:
            current_time (int): The current time in milliseconds.
            last_rotation_time (int): The last time the Tetrimino was rotated.
            rotation_delay (int): The minimum delay required between rotations.
            rotate_sound (pygame.mixer.Sound): Sound to play upon rotation.

        Returns:
            int: The updated last rotation time.
        """
        if current_time - last_rotation_time > rotation_delay:
            next_rotation = (self.rotation + 1) % len(self.rotations)
            if self.can_fit(self.position[0], self.position[1], next_rotation):
                self.rotation = next_rotation
                if rotate_sound:
                    rotate_sound.play()
                return current_time
        return last_rotation_time

    def can_fit(self, row, col, rotation=None):
        """
        Check if the Tetrimino can fit in the grid at the specified position with the given rotation.

        Args:
            row (int): The row index on the grid.
            col (int): The column index on the grid.
            rotation (int, optional): The rotation index. Defaults to current rotation if None.

        Returns:
            bool: True if the Tetrimino can fit, False otherwise.
        """
        if rotation is None:
            rotation = self.rotation
        shape = self.rotations[rotation][0]
        for i, line in enumerate(shape):
            for j, cell in enumerate(line):
                if cell > 0:
                    r, c = row + i, col + j
                    if r >= len(self.grid) or c < 0 or c >= len(self.grid[0]) or self.grid[r][c]:
                        return False
        return True

    def get_current_shape(self):
        """
        Get the matrix representing the current rotation of the Tetrimino.

        Returns:
            list of list of int: The 2D matrix for the current rotation.
        """
        return self.rotations[self.rotation][0]  # Return the current rotation shape
