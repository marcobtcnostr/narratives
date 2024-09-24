"""
This...
"""

# processor/summarisation.py

import logging
import openai
from fpdf import FPDF
import os
import time
import re


class Summariser:
    def __init__(self, api_key_path='openai_api_key.txt'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api_key = self.load_api_key(api_key_path)
        self.client = openai.OpenAI(api_key=self.api_key)

    # def make_api_call(self, method, *args, **kwargs):
    #     """
    #     A wrapper around the OpenAI API call to handle rate limiting.
    #     'method' could be one of the OpenAI client's methods like 'create', 'retrieve', etc.
    #     """
    #     response = method(*args, **kwargs)
    #     # This is conceptual; you'll need to access the actual headers from the response
    #     rate_limit_headers = self.parse_rate_limit_headers(response.headers)
    #     if rate_limit_headers['remaining'] == 0:
    #         reset_time = rate_limit_headers['reset']
    #         self.logger.info(f"Rate limit reached. Waiting for {reset_time} seconds.")
    #         time.sleep(reset_time)
    #     return response

    # def parse_rate_limit_headers(self, headers):
    #     """
    #     Parse the rate limit headers from the response.
    #     You need to implement this based on how the OpenAI client exposes headers.
    #     """
    #     limit = int(headers.get('x-ratelimit-limit-requests', 0))
    #     remaining = int(headers.get('x-ratelimit-remaining-requests', 0))
    #     reset = int(headers.get('x-ratelimit-reset-requests', 0))  # Reset time in seconds
    #     return {'limit': limit, 'remaining': remaining, 'reset': reset}

    def load_api_key(self, filepath):
        try:
            with open(filepath, 'r') as file:
                self.logger.info(f"Loaded API key")
                return file.read().strip()
        except Exception as e:
            self.logger.error(f"Failed to load API key: {e}")
            raise

    def create_pdf(self, text, filename):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, text)
            pdf.output(filename)
            # Ensure the PDF is fully written
            while not os.path.exists(filename):
                time.sleep(1)
            self.logger.info(f"Created PDF: {filename}")
        except Exception as e:
            self.logger.error(f"Failed to create PDF: {e}")
            raise

    def delete_pdf(self, pdf_filename):
        try:
            os.remove(pdf_filename)
            self.logger.info(f"Deleted PDF: {pdf_filename}")
        except FileNotFoundError:
            self.logger.warning(f"PDF file not found, could not delete: {pdf_filename}")
        except Exception as e:
            self.logger.error(f"Unexpected error deleting PDF {pdf_filename}: {e}")
            raise

    def upload_file(self, pdf_filename):
        try:
            with open(pdf_filename, "rb") as pdf_file:
                file = self.client.files.create(
                    file=pdf_file, purpose="assistants")
            self.logger.info(f"Uploaded: {file} to OpenAI")

            time.sleep(5)

            return file
        except Exception as e:
            self.logger.error(f"Failed to upload file to assistant: {e}")
            raise

    def create_assistant(self, file_id):
        try:
            assistant = self.client.beta.assistants.create(
                model="gpt-3.5-turbo-1106",
                name="SummaryDemo",
                description="Analyze news articles and categorize content into Facts, Opinions, and Predictions."
            )
            assistant = self.client.beta.assistants.update(
                assistant_id=assistant.id,
                tools=[{"type": "retrieval"}],
                file_ids=[file_id],
            )
            self.logger.info(f"Created assistant: {assistant}")
            return assistant
        except Exception as e:
            self.logger.error(f"Failed to create assistant: {e}")
            raise

    def create_thread_and_summarise(self, assistant_id):
        try:
            thread = self.client.beta.threads.create()
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content="Please analyze and summarize synthetically the attached document and categorize its content into"
                        " Facts, Opinions, and Predictions as per the given instructions."
            )
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id, assistant_id=assistant_id)
            
            time.sleep(5)

            summary = self.wait_for_run_completion(run, thread.id)
            self.logger.info(f"Created summary")
            return summary
        except Exception as e:
            self.logger.error(f"Failed to create thread and summarise: {e}")
            raise

    def create_thread_and_analyse_sentiment(self, assistant_id):
        try:
            thread = self.client.beta.threads.create()
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content="Please analyze the sentiment analysis score of the attached document and return its score in a scale between -1 to +1"
                        " where -1 is the most negative sentiment and +1 is the most positive sentiment score!"
                        " The output must have the following format: 'The sentiment analysis score of this document is: (number on a scale between -1 and +1)'"
                        " The output score MUST be a number between -1 and +1, this is extremely important."
            )

            time.sleep(5)

            run = self.client.beta.threads.runs.create(
                thread_id=thread.id, assistant_id=assistant_id)

            sentiment_analysis = self.wait_for_run_completion(run, thread.id)
            # Regex pattern to match numbers
            pattern = re.compile(r"[-+]?\d*\.\d+|\d+")
            match = pattern.search(sentiment_analysis)
            if match:
                # Return the first found number as float
                sentiment_analysis = float(match.group())
            else:
                sentiment_analysis = None
            
            self.logger.info(f"Created sentiment analysis")

            return sentiment_analysis
        except Exception as e:
            self.logger.error(f"Failed to create thread and analyse sentiment: {e}")
            raise

    def wait_for_run_completion(self, run, thread_id, timeout=60):
        """Polls for run completion with a timeout."""
        self.logger.info("Starting to wait for run completion.")
        start_time = time.time()
        while time.time() - start_time < timeout:
            run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            self.logger.debug(f"Checked run status: {run.status}")
            if run.status not in ["queued", "in_progress"]:
                self.logger.info("Run completed, waiting for assistant response.")
                return self.wait_for_assistant_response(thread_id)
            time.sleep(2)  # Poll every 2 seconds
        self.logger.error("Timeout occurred while waiting for run to complete.")
        raise TimeoutError("Timeout waiting for run to complete")

    def wait_for_assistant_response(self, thread_id, timeout=60):
        """Polls for assistant's response with a timeout."""
        self.logger.info("Waiting for assistant's response.")
        start_time = time.time()
        while time.time() - start_time < timeout:
            messages = self.client.beta.threads.messages.list(thread_id=thread_id, order="asc")
            if len(messages.data) >= 2:
                assistant_message = messages.data[1]
                if assistant_message.content and assistant_message.content[0].text.value.strip() != "":
                    self.logger.info("Received assistant's response.")
                    return assistant_message.content[0].text.value
            self.logger.debug("Still waiting for assistant's response...")
            time.sleep(2)  # Poll every 2 seconds
        self.logger.error("Timeout occurred while waiting for assistant's response.")
        raise TimeoutError("Timeout waiting for assistant response")


    def upload_file_summarise_and_analyse_sentiment(self, pdf_filename):
        file = self.upload_file(pdf_filename)
        assistant = self.create_assistant(file.id)
        summary = self.create_thread_and_summarise(assistant.id)
        sentiment_analysis = self.create_thread_and_analyse_sentiment(assistant.id)
        self.cleanup(file.id, assistant.id)
        return summary, sentiment_analysis

    def cleanup(self, file_id, assistant_id):
        try:
            self.client.beta.assistants.files.delete(
                assistant_id=assistant_id, file_id=file_id)
            self.client.beta.assistants.delete(assistant_id)
            self.client.files.delete(file_id)
            self.logger.info(f"Cleanup files and assistant")
        except Exception as e:
            self.logger.error(f"Failed to cleanup files and assistant: {e}")
            raise

    def process_text(self, text):
        pdf_filename = "temp_file.pdf"
        self.create_pdf(text, pdf_filename)
        summary, sentiment_analysis = self.upload_file_summarise_and_analyse_sentiment(
            pdf_filename)
        self.delete_pdf(pdf_filename)

        time.sleep(15)

        return summary, sentiment_analysis


# if __name__ == "__main__":
#     summariser = Summariser()
#     text_to_process = "In a quaint village nestled among rolling hills, there lived a young girl named Lily. She had a unique gift of speaking to animals, a secret she kept hidden from everyone.  Each day, after her chores, Lily would wander into the nearby woods, where her friends, the woodland creatures, eagerly awaited her. One day, a mysterious, shimmering bird appeared, leading Lily to a hidden part of the forest she'd never explored. There, she discovered a crystal-clear pond whose waters glittered under the sun. The bird, which was actually a guardian of the forest, revealed that the pond held magical properties and could grant a single wish. Lily thought hard. She could ask for wealth, fame, or any number of things. But looking around at her animal friends, she realized she already had what mattered most. She wished instead for the wellbeing and protection of the forest and its inhabitants. As the words left her lips, the pond's waters glowed brightly, and a wave of energy swept through the woods. From that day on, the forest thrived like never before, and Lily's bond with her animal friends grew even stronger. She had found true happiness not in seeking for herself, but in caring for others."
#     summary, sentiment_analysis = summariser.process_text(text_to_process)
#     print(f"Summary: {summary}")
#     print(f"Sentiment analysis: {sentiment_analysis}")
