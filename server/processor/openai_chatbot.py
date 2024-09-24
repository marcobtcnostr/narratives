"""
This...
"""

# processor\openai_chatbot.py

import openai
import time
import logging
import sqlite3
import os
import re

class OpenAIChatbot:
    def __init__(self, db_path='narratives.db'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api_key = self.load_api_key_from_db(db_path)
        self.client = openai.OpenAI(api_key=self.api_key)
        self.thread_id = None
        self.assistant_id = None
        self.db_path = db_path

    def load_api_key_from_db(self, db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT key FROM api_keys WHERE api = ?", ('openai_api_key',))
            result = cursor.fetchone()
            conn.close()
            if result:
                self.logger.info(f"Loaded API key from database")
                return result[0]
            else:
                raise ValueError("API key for 'openai_api_key' not found in the database")
        except Exception as e:
            self.logger.error(f"Failed to load API key from database: {e}")
            raise

    def create_assistant(self):
        try:
            assistant = self.client.beta.assistants.create(
                model="gpt-3.5-turbo-1106",
                name="ChatAssistant",
                description="An AI assistant for interactive chat with retrieval capabilities."
            )
            assistant = self.client.beta.assistants.update(
                assistant_id=assistant.id,
                tools=[{"type": "retrieval"}]
            )
            self.assistant_id = assistant.id
            return assistant
        except Exception as e:
            self.logger.error(f"Failed to create assistant with retrieval: {e}")
            raise

    def delete_assistant(self):
        if self.assistant_id:
            try:
                self.client.beta.assistants.delete(self.assistant_id)
                self.assistant_id = None
            except Exception as e:
                self.logger.error(f"Failed to delete assistant: {e}")

    def sanitize_filename(self, title):
        """Remove or replace characters not allowed in filenames."""
        return re.sub(r'[\\/*?:"<>|]', "", title)

    def load_files_for_retrieval(self, content_ids):
        # Connect to the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Prepare the query to select content based on content_ids
        placeholders = ', '.join(['?'] * len(content_ids))
        query = f"SELECT content_id, title, summary FROM library WHERE content_id IN ({placeholders})"
        
        cursor.execute(query, content_ids)
        rows = cursor.fetchall()

        file_ids = []

        # For each selected content, generate a file and upload it
        for row in rows:
            content_id, title, summary = row
            safe_title = self.sanitize_filename(title)
            filename = f"{safe_title}_tmp.txt"
            with open(filename, 'w') as f:
                f.write(summary)

            # Upload the file to OpenAI
            with open(filename, 'rb') as f:
                uploaded_file = self.client.files.create(
                    file=f,
                    purpose='assistants'
                )
                file_ids.append(uploaded_file.id)

            # Optionally, remove the file after uploading
            os.remove(filename)

        # Update the assistant with the uploaded file IDs for retrieval
        if file_ids:
            self.client.beta.assistants.update(
                self.assistant_id,
                tools=[{"type": "retrieval"}],
                file_ids=file_ids,
            )

        conn.close()

    def process_chat_message(self, user_message):
        if not self.thread_id:
            self.thread_id = self.client.beta.threads.create().id
            
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=user_message
        )
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id,
        )
        # Poll the OpenAI API for the response
        response_message = self.wait_for_run_completion(run, self.thread_id)
        return response_message

    def wait_for_run_completion(self, run, thread_id, timeout=600):
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

    def wait_for_assistant_response(self, thread_id, timeout=600):
        """Polls for assistant's response with a timeout."""
        self.logger.info("Waiting for assistant's response.")
        start_time = time.time()
        while time.time() - start_time < timeout:
            messages = self.client.beta.threads.messages.list(thread_id=thread_id, order="asc")
            # Find the last message from the assistant, which should be the latest response
            if messages and isinstance(messages.data, list) and len(messages.data) > 0:
                last_message = messages.data[-1]  # Adjust to get the last message in the list
                if last_message.role == "assistant":  # Ensure the message is from the assistant
                    if last_message.content and isinstance(last_message.content, list) and len(last_message.content) > 0:
                        response_message = last_message.content[0].text.value
                        self.logger.info("Received assistant's response.")
                        return response_message
            self.logger.debug("Still waiting for assistant's response...")
            time.sleep(2)  # Poll every 2 seconds
        self.logger.error("Timeout occurred while waiting for assistant's response.")
        raise TimeoutError("Timeout waiting for assistant response")

    # Destructor to delete the assistant and thread
    def __del__(self):
        self.delete_assistant()
        self.thread_id = None

# if __name__ == "__main__":
#     # Initialize the chatbot handler with the path to your OpenAI API key
#     chatbot_handler = OpenAIChatbot(api_key_path='openai_api_key.txt')
#     chatbot_handler.create_assistant()  # Create a new assistant
#     chatbot_handler.load_files_for_retrieval(['https://www.bbc.co.uk/news/business-68489236', 'https://www.bbc.co.uk/news/business-68271274'])

#     try:
#         # Start a conversation with the chatbot
#         while True:
#             # Get input message from the user
#             user_message = input("You: ")
#             if user_message.lower() == 'exit':  # type 'exit' when you want to end the chat
#                 print("Exiting chat.")
#                 break

#             # Send message and get response from the chatbot
#             response_message = chatbot_handler.process_chat_message(user_message)
            
#             print(f"Chatbot: {response_message}")
#     finally:
#         # Clean up by deleting the assistant
#         chatbot_handler.delete_assistant()
