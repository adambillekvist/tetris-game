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

class InputHandler:
    """Handles user input and translates it into game commands that affect the game state.

    Attributes:
        game_logic (GameLogic): A reference to the game's logic handler to directly affect game state.
        commands (dict): A dictionary to keep track of active commands based on user input.
    """
    def __init__(self, game_logic):
        """
        Initialize the InputHandler with a reference to the game's logic controller.

        Args:
            game_logic (GameLogic): The game logic controller which handles game state updates.
        """
        self.game_logic = game_logic  # Pass a reference to the GameLogic object
        self.commands = {}

    def process_event(self, event):
        """
        Processes a single pygame event and updates commands based on the event type.

        Args:
            event (pygame.Event): The event to process, typically received from pygame.event.get().
        """
        if event.type == pygame.KEYDOWN:
            # Handling key press events
            if event.key == pygame.K_LEFT:
                self.commands['move_left'] = True
            elif event.key == pygame.K_RIGHT:
                self.commands['move_right'] = True
            elif event.key == pygame.K_DOWN:
                self.commands['move_down'] = True
            elif event.key == pygame.K_UP:
                self.commands['rotate'] = True
            elif event.key == pygame.K_p:
                # Toggle pause when 'p' is pressed
                self.game_logic.toggle_pause()
            elif event.key == pygame.K_r:  
                # Reset the game when 'r' is pressed
                self.game_logic.reset_game()

        elif event.type == pygame.KEYUP:
            # Handling key release events
            if event.key == pygame.K_LEFT:
                self.commands.pop('move_left', None)
            elif event.key == pygame.K_RIGHT:
                self.commands.pop('move_right', None)
            elif event.key == pygame.K_DOWN:
                self.commands.pop('move_down', None)
            elif event.key == pygame.K_UP:
                self.commands.pop('rotate', None)