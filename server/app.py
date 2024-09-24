import threading
import tkinter as tk
from waitress import serve
from logging_config import setup_logging
from gui.server_gui import ServerGUI
import json
import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from db.db_manager import DBManager
from processor.openai_chatbot import OpenAIChatbot

# Flask app definition
app = Flask(__name__)
CORS(app)

ENVIRONMENT = 'development'  # 'development' or 'production'

# Call the setup_logging function at the beginning
setup_logging(ENVIRONMENT)

db_manager = DBManager('narratives.db')
db_manager.connect()
db_manager.create_library_table()
db_manager.create_publisher_options_table()
db_manager.create_api_keys_table()
db_manager.close()

# Initialize the Chatbot Handler globally but don't create the assistant yet.
chatbot_handler = OpenAIChatbot(db_path='narratives.db')


@app.route('/fetch-api-keys', methods=['GET'])
def fetch_api_keys():
    try:
        db_manager.connect()
        api_keys = db_manager.fetch_api_keys()
        db_manager.close()
        return jsonify(api_keys), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update-api-key', methods=['POST'])
def update_api_key():
    try:
        data = request.json
        api = data.get('api')
        key = data.get('key')
        db_manager.connect()
        db_manager.update_api_key(api, key)
        db_manager.close()
        return jsonify({"message": "API key updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update-narratives-database', methods=['POST'])
def update_narratives_database():
    try:
        db_manager.connect()

        # Fetch all content IDs with empty transcripts
        unprocessed_content_ids = db_manager.fetch_unprocessed_content_ids()

        for content_id in unprocessed_content_ids:
            db_manager.scrape_content_id(content_id)
            db_manager.process_content_id(content_id)

        db_manager.close()

        return jsonify({"message": "Database updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/fetch-narratives-data', methods=['POST'])
def fetch_narratives():
    filters = request.json.get('filters', {})
    data = db_manager.fetch_filtered_data(filters)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Data not found"}), 404


@app.route('/fetch-publisher-options', methods=['GET'])
def fetch_publisher_options():
    publisher_options = db_manager.fetch_publisher_options()
    if publisher_options:
        return jsonify(publisher_options), 200
    else:
        return jsonify({"error": "No publisher options found"}), 404


@app.route('/edit-publisher-options', methods=['POST'])
def edit_publisher_options():
    try:
        updates = request.json.get('publisherOptions', [])
        db_manager.connect()
        for update in updates:
            publisher = update.get('publisher')
            publisher_political_orientation = update.get('publisher_political_orientation')
            country = update.get('country')
            db_manager.edit_publisher_option(publisher, publisher_political_orientation, country)
        db_manager.close()

        return jsonify({"message": "Publisher options updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add-content-id', methods=['POST'])
def add_content_id():
    try:
        content_id = request.json.get('content_id')

        db_manager.connect()
        added = db_manager.add_content_id(content_id)
        db_manager.close()

        if added:
            return jsonify({"message": "Content ID added successfully"}), 200
        else:
            return jsonify({"message": "Content ID already exists"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update-content-id-topic', methods=['POST'])
def update_content_id_topic():
    try:
        data = request.json
        content_id = data.get('content_id')
        new_topic = data.get('topic')

        db_manager.connect()
        db_manager.update_content_id_topic(content_id, new_topic)
        db_manager.close()

        return jsonify({"message": "Article topic updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/load-content-for-openai-chatbot', methods=['POST'])
def load_content_for_chatbot():
    try:
        content_ids = request.json.get('content_ids')

        # Delete the existing assistant if there is one
        chatbot_handler.delete_assistant()

        # Create a new assistant and load content for it
        chatbot_handler.create_assistant()
        chatbot_handler.load_files_for_retrieval(content_ids)

        return jsonify({"message": "New chatbot assistant created and files loaded successfully"}), 200
    except Exception as e:
        app.logger.error(f"Failed to load content for chatbot: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/chat-with-openai-assistant', methods=['POST'])
def chat_with_assistant():
    try:
        user_message = request.json.get('message')
        response_message = chatbot_handler.process_chat_message(user_message)
        return jsonify({"response": response_message}), 200
    except Exception as e:
        app.logger.error(f"Error chatting with assistant: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/close-openai-chat', methods=['POST'])
def close_chat():
    try:
        chatbot_handler.delete_assistant()
        return jsonify({"message": "Chat closed and assistant deleted successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error closing chat: {str(e)}")
        return jsonify({"error": str(e)}), 500


def run_server():
    """
    Run the Flask server using Waitress for production or Flask's built-in server in development.
    """
    if ENVIRONMENT == 'production':
        serve(app, host='0.0.0.0', port=5000)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


# Main function to run the GUI
def main():
    root = tk.Tk()
    gui = ServerGUI(root, run_server)
    root.mainloop()


if __name__ == '__main__':
    main()