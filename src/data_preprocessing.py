# src/data_preprocessing.py
import re
import json
import os
import pandas as pd

class TextCleaner:
    """
    A class to handle the complete text cleaning pipeline, including
    noise removal, slang normalization, and stopword removal.
    """
    def __init__(self, resources_path='src/resources/NLP_bahasa_resources'):
        """
        Initializes the cleaner by loading slang and stopword dictionaries.
        
        Args:
            resources_path (str): The path to the directory containing dictionary files.
        """
        slang_path = os.path.join(resources_path, 'combined_slang_words.txt')
        stopwords_path = os.path.join(resources_path, 'combined_stop_words.txt')
        
        self.slang_dict = self._load_json_dict(slang_path)
        self.stopwords = self._load_set(stopwords_path)
        print("✅ TextCleaner initialized with slang and stopword dictionaries.")

    def _load_json_dict(self, filepath):
        """Loads a JSON file into a dictionary."""
        try:
            with open(filepath, 'r', encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ WARNING: Dictionary file not found at {filepath}. Slang normalization will be skipped.")
            return {}
        except json.JSONDecodeError:
            print(f"⚠️ WARNING: Failed to decode JSON from {filepath}. Slang normalization will be skipped.")
            return {}

    def _load_set(self, filepath):
        """Loads a text file into a set, with each line as an element."""
        try:
            with open(filepath, 'r', encoding="utf-8") as f:
                return set(f.read().splitlines())
        except FileNotFoundError:
            print(f"⚠️ WARNING: Stopwords file not found at {filepath}. Stopword removal will be skipped.")
            return set()

    def clean(self, text: str) -> str:
        """
        Applies the full cleaning pipeline to a string.

        Args:
            text (str): The input string to clean.

        Returns:
            str: The fully cleaned and normalized string.
        """
        if not isinstance(text, str):
            return ""

        # Step 1: Remove noise (lowercase, URLs, mentions, special chars, emojis)
        text = text.lower()
        text = re.sub(r'http\S+|www.\S+', '', text) # Remove URLs
        text = re.sub(r'@\w+', '', text) # Remove mentions
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # Remove special characters
        text = re.sub(r'[^\x00-\x7F]+', '', text) # Remove emojis
        text = text.strip()

        # Step 2 & 3: Normalize slang and remove stopwords in a single pass
        words = text.split()
        normalized_words = [
            self.slang_dict.get(word, word) for word in words if word not in self.stopwords
        ]
        
        return ' '.join(normalized_words)

# For direct use in other scripts, you can create a default instance
# This is a simple way to use it, but initializing it once in the main
# scripts (train.py, main.py) is more efficient.
default_cleaner = TextCleaner()
clean_text = default_cleaner.clean

