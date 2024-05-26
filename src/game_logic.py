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

import random
import pygame
from .tetrimino import Tetrimino
from . import settings

class GameLogic:
    """Main class for handling the logic of the Tetris game, managing game states, and responding to player actions.

    Attributes:
        break_line_sound (pygame.mixer.Sound): Sound played when a line is cleared.
        rotate_sound (pygame.mixer.Sound): Sound played when a tetrimino is rotated.
        grid (list of list of int): Representation of the game grid.
        score (int): Current score of the player.
        lines_cleared (int): Total number of lines cleared.
        level (int): Current level of the game.
        current_tetrimino (Tetrimino): The currently active tetrimino.
        game_over (bool): Flag indicating if the game has ended.
        is_paused (bool): Flag indicating if the game is paused.
        drop_speed (int): Time in milliseconds between automatic drops of the tetrimino.
        soft_drop_speed (int): Time in milliseconds for quicker drops when moving down is held.
        move_speed (int): Time in milliseconds between lateral movements when arrow keys are held.
        rotation_delay (int): Time in milliseconds between rotations.
        last_drop_time (int): Last recorded time when a tetrimino was dropped.
        last_move_time (int): Last recorded time when a tetrimino was moved laterally.
        last_rotation_time (int): Last recorded time when a tetrimino was rotated.
    """
    def __init__(self, break_line_sound, rotate_sound):
        """
        Initializes the game logic component with necessary sound effects and starting configurations.
        """
        self.rotate_sound = rotate_sound
        self.break_line_sound = break_line_sound
        self.grid = [[0]*settings.GRID_WIDTH for _ in range(settings.GRID_HEIGHT)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.current_tetrimino = self.new_tetrimino()
        self.game_over = False
        self.is_paused = False
        self.drop_speed = 1000
        self.soft_drop_speed = 50
        self.move_speed = 100
        self.rotation_delay = 200
        self.last_drop_time = pygame.time.get_ticks()
        self.last_move_time = pygame.time.get_ticks()
        self.last_rotation_time = pygame.time.get_ticks()

    def toggle_pause(self):
        """
        Toggles the pause state of the game.
        """
        self.is_paused = not self.is_paused
        return self.is_paused

    def reset_game(self):
        """
        Resets the game to the initial state, clearing the grid and resetting scores and level.
        """
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.current_tetrimino = self.new_tetrimino()
        self.game_over = False
        self.is_paused = False

    def update_level(self):
        """
        Updates the game level based on the number of lines cleared, increasing the difficulty.
        """
        new_level = 1 + self.lines_cleared // settings.LEVEL_CHANGE_LINES
        if new_level > self.level:
            self.level = new_level
            self.adjust_game_speed()

    def adjust_game_speed(self):
        """
        Adjusts the speed of the game based on the current level, affecting how quickly tetriminos fall.
        """
        self.drop_speed = max(100, self.drop_speed - settings.LEVEL_SPEED_INCREMENT * (self.level - 1))
   
    def new_tetrimino(self):
        """
        Create a new tetrimino and place it at the starting position.
        """
        tetrimino_type = random.choice(list(settings.TETRIMINOS.keys()))
        tetrimino = Tetrimino(tetrimino_type, self.grid)
        if not tetrimino.can_fit(0, 4):
            self.game_over = True
        return tetrimino
    
    def update(self, commands):
        """
        Main update loop of the game logic, called every frame to process input, drop tetriminos, and check game state.
        """
        if self.game_over or self.is_paused:
            return

        current_time = pygame.time.get_ticks()
        self.process_player_input(current_time, commands)
        self.handle_automatic_drop(current_time, commands)

    def process_player_input(self, current_time, commands):
        """
        Processes player inputs for moving and rotating tetriminos.
        """
        self.handle_moves(current_time, commands)
        self.handle_rotation(current_time, commands)

    def handle_moves(self, current_time, commands):
        """
        Handles horizontal movements based on player commands.
        """
        if current_time - self.last_move_time > self.move_speed:
            if 'move_left' in commands and self.current_tetrimino.can_fit(self.current_tetrimino.position[0], self.current_tetrimino.position[1] - 1):
                self.current_tetrimino.position[1] -= 1
            if 'move_right' in commands and self.current_tetrimino.can_fit(self.current_tetrimino.position[0], self.current_tetrimino.position[1] + 1):
                self.current_tetrimino.position[1] += 1
            self.last_move_time = current_time

    def handle_rotation(self, current_time, commands):
        """
        Handles the rotation of tetriminos based on player commands.
        """
        if 'rotate' in commands:
            self.last_rotation_time = self.current_tetrimino.rotate(current_time, self.last_rotation_time, self.rotation_delay, self.rotate_sound)

    def handle_automatic_drop(self, current_time, commands):
        """
        Manages the automatic dropping of tetriminos based on the game's drop speed and player's soft drop commands.
        """
        if 'move_down' in commands:
            if current_time - self.last_drop_time > self.soft_drop_speed:
                self.attempt_to_drop(current_time)
        elif current_time - self.last_drop_time > self.drop_speed:
            self.attempt_to_drop(current_time)

    def attempt_to_drop(self, current_time):
        """
        Attempts to drop the tetrimino one level; if it cannot drop further, it is placed and the grid is updated.
        """
        if not self.drop_tetrimino():
            self.place_tetrimino()
            self.clear_lines()
            self.current_tetrimino = self.new_tetrimino()
        self.last_drop_time = current_time

    def drop_tetrimino(self):
        """
        Drops the current tetrimino by one level if possible, places it if it reaches the bottom or hits another tetrimino.
        """
        if self.current_tetrimino.can_fit(self.current_tetrimino.position[0] + 1, self.current_tetrimino.position[1]):
            self.current_tetrimino.position[0] += 1
            if not self.current_tetrimino.can_fit(self.current_tetrimino.position[0] + 1, self.current_tetrimino.position[1]):
                self.place_tetrimino()
                self.clear_lines()
                self.update_level()
                self.current_tetrimino = self.new_tetrimino()
                if not self.current_tetrimino.can_fit(0, 4):
                    self.game_over = True
            return True
        return False

    def place_tetrimino(self):
        """
        Places the current tetrimino onto the grid, marking its cells as occupied.
        """
        shape = self.current_tetrimino.get_current_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell > 0:
                    self.grid[self.current_tetrimino.position[0] + i][self.current_tetrimino.position[1] + j] = cell

    def clear_lines(self):
        """
        Clears completed lines from the grid, increases the score, and plays a sound effect.
        """
        cleared_lines = 0
        new_grid = []
        for row in self.grid:
            if 0 in row:
                new_grid.append(row)
            else:
                cleared_lines += 1
        if cleared_lines > 0:
            self.break_line_sound.play()
            
        new_grid = [[0]*settings.GRID_WIDTH for _ in range(cleared_lines)] + new_grid
        self.grid = new_grid
        self.lines_cleared += cleared_lines
        self.score += cleared_lines ** 2

    def check_game_over(self):
        """
        Checks if the game should end because a new tetrimino cannot be placed at the starting position.
        """

        if not self.current_tetrimino.can_fit(0, 4):
            self.game_over = True
        return self.game_over