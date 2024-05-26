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
import sys
import random
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MUTE, ROTATE_SOUND, BREAK_LINE_SOUND, GAME_OVER_SOUND, WHITE
from src.game_logic import GameLogic
from src.display import Display
from src.input_handler import InputHandler
from src import HighscoreManager

def show_menu(screen, break_line_sound, game_over_sound, rotate_sound):
    """
    Display the main menu and handle menu interactions.
    
    Args:
        screen (pygame.Surface): The main game screen.
        break_line_sound (pygame.mixer.Sound): Sound effect for line clearing.
        game_over_sound (pygame.mixer.Sound): Sound effect for game over.
        rotate_sound (pygame.mixer.Sound): Sound effect for tetrimino rotation.
    """
    menu_running = True
    font = pygame.font.Font(None, 36)
    highscore_manager = HighscoreManager()
    highscore = highscore_manager.get_highscore()

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:     # Start the game
                    menu_running = False
                elif event.key == pygame.K_q:   # Quit the game
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))  # Clear screen
        
        # Display Menu Text
        start_text = font.render('Press S to Start', True, (255, 255, 255))
        quit_text = font.render('Press Q to Quit', True, (255, 255, 255))
        highscore_text = f"Highscore: {highscore}"
        
        start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 25))
        quit_text_rect = quit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 25))
        screen.blit(start_text, start_text_rect)
        screen.blit(quit_text, quit_text_rect)
        
        # Display highscore with each letter in different colors
        highscore_text = f"Highscore: {highscore}"
        x_start = SCREEN_WIDTH / 2 - font.size(highscore_text)[0] / 2  # Center the text
        y_start = SCREEN_HEIGHT / 2 - 150
        for char in highscore_text:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            rendered_char = font.render(char, True, color)
            char_rect = rendered_char.get_rect(left=x_start, top=y_start)
            screen.blit(rendered_char, char_rect)
            x_start += font.size(char)[0]  # Move x_start to the right by the width of the character

        pygame.display.flip()

    # Transition to game if menu loop exits
    main_game(screen, break_line_sound, game_over_sound, rotate_sound)

def main_game(screen, break_line_sound, game_over_sound, rotate_sound):
    """
    Manage the main game loop and gameplay interactions.

    Args:
        screen (pygame.Surface): The main game screen.
        break_line_sound (pygame.mixer.Sound): Sound effect for line clearing.
        game_over_sound (pygame.mixer.Sound): Sound effect for game over.
        rotate_sound (pygame.mixer.Sound): Sound effect for tetrimino rotation.
    """
    clock = pygame.time.Clock()
    game_logic = GameLogic(break_line_sound, rotate_sound)
    display = Display(screen)
    input_handler = InputHandler(game_logic)
    highscore_manager = HighscoreManager()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            input_handler.process_event(event)

        # Update and render game state
        if not game_logic.is_paused:
            game_logic.update(input_handler.commands)
            display.render(game_logic.grid, game_logic.score, game_logic.current_tetrimino, game_logic.level, game_logic.is_paused)
        else:
            display.render(game_logic.grid, game_logic.score, game_logic.current_tetrimino, game_logic.level, game_logic.is_paused)

        # Handle game over sequence
        if game_logic.check_game_over():
            game_over_sound.play()
            display.show_game_over()
            highscore_manager.update_highscore(game_logic.score)
            running = False  # Stop the game loop if game is over

        pygame.display.flip()
        clock.tick(FPS)  # Maintain the frame rate

    # Return to menu after game over
    show_menu(screen, break_line_sound, game_over_sound, rotate_sound)

def main():
    """
    Initialize the game and create the main window.
    """
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    
    # Load sounds if not muted
    break_line_sound = game_over_sound = rotate_sound = None
    if not MUTE:
        break_line_sound = pygame.mixer.Sound(BREAK_LINE_SOUND)
        game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)
        rotate_sound = pygame.mixer.Sound(ROTATE_SOUND)

    show_menu(screen, break_line_sound, game_over_sound, rotate_sound)

if __name__ == "__main__":
    main()