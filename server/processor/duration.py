"""
This...
"""

# processor/duration.py

import math

class Duration:
    def __init__(self):
        # Assuming an average reading speed of 300 words per minute
        self.words_per_minute = 200

    def analyse_duration(self, text):
        word_count = self.count_words(text)
        # Calculate the duration in minutes and round up to the nearest minute
        duration_in_minutes = math.ceil(word_count / self.words_per_minute)
        return duration_in_minutes

    @staticmethod
    def count_words(text):
        # Split the text into words and count them
        words = text.split()
        return len(words)
