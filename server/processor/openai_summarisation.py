"""
This...
"""

# processor\openai_summarisation.py

import logging
import openai
import sqlite3

class OpenAISummariser:
    def __init__(self, db_path='narratives.db'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api_key = self.load_api_key_from_db(db_path)
        self.client = openai.OpenAI(api_key=self.api_key)

    def load_api_key_from_db(self, db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT key FROM api_keys WHERE api = ?", ('openai_api_key',))
            result = cursor.fetchone()
            conn.close()
            if result:
                self.logger.info("Loaded API key from database")
                return result[0]
            else:
                raise ValueError("API key for 'openai_api_key' not found in the database")
        except Exception as e:
            self.logger.error(f"Failed to load API key from database: {e}")
            raise

    def chunk_text(self, text, max_chunk_size=1000):
        """Splits the text into manageable chunks."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            if current_length + len(word) > max_chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1  # Include space

        # Add the last chunk if it contains any words
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def recursive_summarize(self, text, instructions, temperature=0.3, max_tokens=1000):
        """Recursively summarizes the text to achieve a more concise summary."""
        conversation = [
            {"role": "system", "content": "You are a highly knowledgeable assistant."},
            {"role": "user", "content": instructions.format(text=text)}
        ]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
            stop=None
        )
        return response.choices[0].message.content

    def process_text(self, text, temperature=0.5, initial_max_tokens=300, final_max_tokens=1000):
        try:
            chunks = self.chunk_text(text)
            summaries = []

            for chunk in chunks:
                summary = self.recursive_summarize(chunk, "Summarize the following text: {text}", temperature, initial_max_tokens)
                summaries.append(summary)

            combined_summary = ' '.join(summaries)

            # final_summary = self.recursive_summarize(combined_summary, "Summarize this text to about 500 words: {text}", temperature, final_max_tokens)
            final_summary = self.recursive_summarize(combined_summary, "Summarizes this text to about 500 words focusing on the main theme, key points, author's sentiment, and conclusions. Includes: 1. Intro Overview, highlighting video's main objective. 2. Key Points, summarizing main discussions. 3. Author's Sentiment, outlining the tone and viewpoint. 4. Conclusions, noting final thoughts and implications. --> {text}", temperature, final_max_tokens)

            self.logger.info("Processed text")
            return final_summary
        except Exception as e:
            self.logger.error(f"Failed to process text: {e}")
            raise

# if __name__ == "__main__":
#     summariser = OpenAISummariser()
#     text_to_process = "In a quaint village nestled among rolling hills, there lived a young girl named Lily. She had a unique gift of speaking to animals, a secret she kept hidden from everyone.  Each day, after her chores, Lily would wander into the nearby woods, where her friends, the woodland creatures, eagerly awaited her. One day, a mysterious, shimmering bird appeared, leading Lily to a hidden part of the forest she'd never explored. There, she discovered a crystal-clear pond whose waters glittered under the sun. The bird, which was actually a guardian of the forest, revealed that the pond held magical properties and could grant a single wish. Lily thought hard. She could ask for wealth, fame, or any number of things. But looking around at her animal friends, she realized she already had what mattered most. She wished instead for the wellbeing and protection of the forest and its inhabitants. As the words left her lips, the pond's waters glowed brightly, and a wave of energy swept through the woods. From that day on, the forest thrived like never before, and Lily's bond with her animal friends grew even stronger. She had found true happiness not in seeking for herself, but in caring for others."
#     summary = summariser.process_text(text_to_process)
#     print(f"Summary: {summary}")
