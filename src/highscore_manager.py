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

class HighscoreManager:
    """Manages the high score for a game, storing and retrieving the high score from a file.

    Attributes:
        filename (str): The name of the file where the high score is saved.
        highscore (int): The highest score achieved that is stored in the file.
    """
    def __init__(self, filename="highscore.txt"):
        """
        Initializes the HighscoreManager with the file name where the high scores are stored.

        Args:
            filename (str, optional): The file name where the high score is saved. Defaults to "highscore.txt".
        """
        self.filename = filename
        self.highscore = self.load_highscore()

    def load_highscore(self):
        """ 
        Load the highscore from a file. If the file doesn't exist, initialize highscore to 0. 
        """
        try:
            with open(self.filename, 'r') as file:
                highscore = int(file.read().strip())
        except (IOError, ValueError):
            highscore = 0
        return highscore

    def update_highscore(self, score):
        """ 
        Update the highscore if the passed score is higher than the existing highscore. 
        """
        if score > self.highscore:
            self.highscore = score
            self.save_highscore()

    def save_highscore(self):
        """ 
        Save the highscore to the file. 
        """
        with open(self.filename, 'w') as file:
            file.write(str(self.highscore))

    def get_highscore(self):
        """
        Retrieves the current high score.
        """
        return self.highscore
