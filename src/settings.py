"""
Tetris Configuration Settings

This module defines the settings and configurations for a Tetris game, including screen dimensions,
game speed, color settings, Tetrimino configurations, and sound settings.

Attributes:
    SCREEN_WIDTH (int): The width of the game screen in pixels.
    SCREEN_HEIGHT (int): The height of the game screen in pixels.
    CELL_SIZE (int): The size of each cell in the grid, representing individual Tetrimino blocks.
    FPS (int): Frames per second, defining the update rate of the game loop.
    BLACK, WHITE, GREY, RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE (tuple): RGB color definitions used throughout the game.
    COLORS (list of tuple): A list mapping Tetrimino types to their respective colors.
    GRID_WIDTH (int): The number of cells horizontally across the game grid.
    GRID_HEIGHT (int): The number of cells vertically across the game grid.
    LEVEL_CHANGE_LINES (int): The number of lines that need to be cleared to trigger a level increase.
    LEVEL_SPEED_INCREMENT (int): The amount of milliseconds by which the fall speed decreases per level increase.
    TETRIMINOS (dict): Definitions of Tetrimino shapes and their rotations.
    MUTE (bool): Flag to mute all game sounds.
    SOUND_VOLUME (float): The volume for sound effects.
    MUSIC_VOLUME (float): The volume for background music.
    BREAK_LINE_SOUND (str): File path to the sound effect for line clearing.
    GAME_OVER_SOUND (str): File path to the sound effect for game over.
    ROTATE_SOUND (str): File path to the sound effect for rotating Tetriminos.
"""

# Screen settings
SCREEN_WIDTH = 400  
SCREEN_HEIGHT = 800  
CELL_SIZE = 40      # Size of each cell in the grid
FPS = 60            # Frames per second

# Color settings (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

COLORS = [
    CYAN,    # I
    BLUE,    # J
    ORANGE,  # L
    YELLOW,  # O
    GREEN,   # S
    RED,     # Z
    MAGENTA  # T
]


# Game settings
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
LEVEL_CHANGE_LINES = 10  # Number of lines cleared to increase the level
LEVEL_SPEED_INCREMENT = 10  # Decrease in fall speed (ms) per level increase

# Define Tetrimino shapes and their rotations
TETRIMINOS = {
    'I': {'rotations': [([[1], [1], [1], [1]], CYAN),
                        ([[1, 1, 1, 1]], CYAN)],
          'color': CYAN},
    'O': {'rotations': [([[2, 2], [2, 2]], YELLOW)],
          'color': YELLOW},
    'T': {'rotations': [([[0, 3, 0], [3, 3, 3]], MAGENTA),
                        ([[3, 0], [3, 3], [3, 0]], MAGENTA),
                        ([[3, 3, 3], [0, 3, 0]], MAGENTA),
                        ([[0, 3], [3, 3], [0, 3]], MAGENTA)],
          'color': MAGENTA},
    'S': {'rotations': [([[0, 4, 4], [4, 4, 0]], GREEN),
                        ([[4, 0], [4, 4], [0, 4]], GREEN)],
          'color': GREEN},
    'Z': {'rotations': [([[5, 5, 0], [0, 5, 5]], RED),
                        ([[0, 5], [5, 5], [5, 0]], RED)],
          'color': RED},
    'J': {'rotations': [([[6, 0, 0], [6, 6, 6]], BLUE),
                        ([[6, 6], [6, 0], [6, 0]], BLUE),
                        ([[6, 6, 6], [0, 0, 6]], BLUE),
                        ([[0, 6], [0, 6], [6, 6]], BLUE)],
          'color': BLUE},
    'L': {'rotations': [([[0, 0, 7], [7, 7, 7]], ORANGE),
                        ([[7, 0], [7, 0], [7, 7]], ORANGE),
                        ([[7, 7, 7], [7, 0, 0]], ORANGE),
                        ([[7, 7], [0, 7], [0, 7]], ORANGE)],
          'color': ORANGE}
}

# Sound settings
MUTE = False
SOUND_VOLUME = 0.5
MUSIC_VOLUME = 0.5
BREAK_LINE_SOUND = 'assets/sounds/line_break.mp3'
GAME_OVER_SOUND = 'assets/sounds/game_over.mp3'
ROTATE_SOUND = 'assets/sounds/rotate_block.mp3'
