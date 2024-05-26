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

import pygame
from . import settings

class Display:
    """Handles the graphical display of the Tetris game state on a pygame window.

    Attributes:
        screen (pygame.Surface): The primary display surface where the game is drawn.
        font (pygame.font.Font): The font used for rendering text in the game.
        cell_size (int): The size of each grid cell, derived from the settings.
    """
    def __init__(self, screen):
        """
        Initialize the display with a specific pygame screen.

        Args:
            screen (pygame.Surface): The pygame display surface where the game elements will be drawn.
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.cell_size = settings.CELL_SIZE
        
    def render(self, grid, score, current_tetrimino, level, is_paused):
        """
        Render the entire game screen, including the grid, active tetrimino, score, and level.

        Args:
            grid (list of list of int): The game grid represented as a 2D array.
            score (int): Current score of the player.
            current_tetrimino (Tetrimino): The currently active tetrimino object.
            level (int): Current level of the game.
            is_paused (bool): True if the game is paused, False otherwise.
        """
        self.screen.fill(settings.BLACK)  # Clear the screen each frame.

        # Draw the grid cells
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if cell:
                    pygame.draw.rect(self.screen, settings.COLORS[cell - 1], rect)
                pygame.draw.rect(self.screen, settings.GREY, rect, 1)

        # Draw the current tetrimino
        if current_tetrimino:
            shape = current_tetrimino.get_current_shape()
            for i, row in enumerate(shape):
                for j, val in enumerate(row):
                    if val:
                        color = settings.COLORS[val - 1]
                        px = (current_tetrimino.position[1] + j) * self.cell_size
                        py = (current_tetrimino.position[0] + i) * self.cell_size
                        pygame.draw.rect(self.screen, color, pygame.Rect(px, py, self.cell_size, self.cell_size))

        # Display score and level at specified positions
        score_text = self.font.render(f"Score: {score}", True, settings.WHITE)
        self.screen.blit(score_text, (settings.CELL_SIZE, settings.CELL_SIZE))  # Margin from top-left corner
        level_text = self.font.render(f"Level: {level}", True, settings.WHITE)
        self.screen.blit(level_text, (settings.CELL_SIZE, settings.CELL_SIZE * 2))  # Slightly below the score
        
        # Handle paused state display
        if is_paused:
            paused_text = self.font.render("Paused", True, (255, 255, 255))
            text_rect = paused_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
            self.screen.blit(paused_text, text_rect)

    def show_paused(self):
        """
        Display the paused state overlay.
        """
        paused_text = self.font.render("Paused", True, settings.WHITE)
        text_rect = paused_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(paused_text, text_rect)

    def show_game_over(self):
        """
        Display the game over screen.
        """
        game_over_text = self.font.render("Game Over!", True, settings.WHITE)
        text_rect = game_over_text.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip() # Update the full display Surface to the screen
        pygame.time.wait(2000)  # Pause the display for 2 seconds to show game over text
