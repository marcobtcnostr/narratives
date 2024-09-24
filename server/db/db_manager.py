"""
This module contains the DBManager class which provides methods for interacting
with a SQLite database. It allows for connecting to the database, creating a
library table, executing queries, and fetching data from the database.
"""

import logging
import sqlite3
import os
from datetime import datetime
from scraper.factory import get_scraper
from processor.factory import get_processor


class DBManager:
    """
    This class...
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect(self):
        """Connect to the SQLite database."""
        if not os.path.isfile(self.db_name):
            self.conn = sqlite3.connect(self.db_name)
        else:
            self.conn = sqlite3.connect(self.db_name)

    def close(self):
        """Close the SQLite database connection."""
        if self.conn:
            self.conn.close()

    def create_library_table(self):
        """Create the library table if it doesn't already exist."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='library'")
        if cursor.fetchone() is None:
            sql_cmd = '''
            CREATE TABLE library (
                content_id VARCHAR(200) PRIMARY KEY,
                title TEXT,
                publisher TEXT,
                author TEXT,
                date_published DATETIME,
                date_added DATETIME,
                duration TEXT,
                platform TEXT,
                transcript TEXT,
                summary TEXT,
                sentiment_analysis REAL,
                macro_topic TEXT,
                publisher_political_orientation TEXT,
                country TEXT,
                sent_by TEXT,
                comments TEXT,
                reference_image TEXT
            );
            '''
            cursor.execute(sql_cmd)
            self.conn.commit()

    def create_publisher_options_table(self):
        """Create the publisher_options table if it doesn't already exist."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='publisher_options'")
        if cursor.fetchone() is None:
            sql_cmd = '''
            CREATE TABLE publisher_options (
                publisher TEXT PRIMARY KEY,
                publisher_political_orientation TEXT,
                country TEXT
            );
            '''
            cursor.execute(sql_cmd)
            self.conn.commit()

    def create_api_keys_table(self):
        """Create the api_keys table if it doesn't already exist."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='api_keys'")
        if cursor.fetchone() is None:
            sql_cmd = '''
            CREATE TABLE api_keys (
                api TEXT PRIMARY KEY,
                key TEXT
            );
            '''
            cursor.execute(sql_cmd)
            self.conn.commit()
        
        # Check if 'openai_api_key' already exists
        cursor.execute("SELECT 1 FROM api_keys WHERE api = ?", ('openai_api_key',))
        if cursor.fetchone() is None:
            # Prepopulate the table with an entry for openai_api_key if it doesn't exist
            cursor.execute("INSERT INTO api_keys (api, key) VALUES (?, ?)", ('openai_api_key', ''))
            self.conn.commit()

    def execute_query(self, query, params=()):
        """Execute a SQL query with optional parameters."""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def query(self, query, params=()):
        """Fetch results from a SQL query with optional parameters."""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def fetch_api_keys(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM api_keys")
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        data_dicts = [dict(zip(columns, row)) for row in data]
        return data_dicts

    def update_api_key(self, api, key):
        query = '''
        INSERT INTO api_keys (api, key)
        VALUES (?, ?)
        ON CONFLICT(api) DO UPDATE SET key = excluded.key
        '''
        self.execute_query(query, (api, key))

    def add_content_id(self, content_id):
        """Add content with the given content_id and set date_added to the current time."""
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            self.connect()
            # Check if content_id already exists
            exists = self.query(
                'SELECT * FROM library WHERE content_id = ?', (content_id,))
            if not exists:
                # Insert new content_id using the existing execute_query method
                self.execute_query(
                    'INSERT INTO library (content_id, date_added) VALUES (?, ?)', (content_id, formatted_time))
                self.logger.info(f"Added content_id = {content_id}")
                return True  # Indicates that the content_id was added
            else:
                self.logger.warning(f"content_id already exists. Skipping {content_id}.")
                return False  # Indicates that the content_id already exists
        finally:
            self.close()
    
    def update_content_id_topic(self, content_id, new_topic):
        query = '''
        UPDATE library
        SET macro_topic = ?
        WHERE content_id = ?
        '''
        self.execute_query(query, (new_topic, content_id))


    def fetch_unprocessed_content_ids(self):
        """Fetch all content IDs from the database where the transcript is empty."""
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute('SELECT content_id FROM library WHERE transcript IS NULL OR transcript = ""')
            unprocessed_content_ids = [row[0] for row in cursor.fetchall()]
            return unprocessed_content_ids
        except sqlite3.Error as e:
            self.logger.error(f"Error fetching unprocessed content IDs. Error: {e}")
            return []
        finally:
            self.close()

    def add_publisher_in_publisher_options(self, publisher):
        """Add a publisher to the publisher_options table if it doesn't already exist."""
        try:
            self.connect()
            exists = self.query(
                'SELECT * FROM publisher_options WHERE publisher = ?', (publisher,))
            if not exists:
                # Insert new publisher
                self.execute_query(
                    'INSERT INTO publisher_options (publisher) VALUES (?)', (publisher,))
                self.logger.info(f"Added new publisher = {publisher}")
        except Exception as e:
            self.logger.error(f"Error adding publisher = {publisher}. Error: {e}")
        finally:
            self.close()

    def scrape_content_id(self, content_id):
        """Scrape the content_id URL to update database fields."""
        scraper = get_scraper(content_id)

        title = scraper.scrape_title()
        transcript = scraper.scrape_transcript()
        date_published = scraper.scrape_date_published()
        publisher = scraper.scrape_publisher()
        reference_image = scraper.scrape_reference_image()

        if "youtube.com" in content_id:
            platform = 'YouTube'
        else:
            platform = 'Web'

        # Check for publisher in publisher_options table
        self.connect()
        publisher_info = self.query(
            'SELECT publisher_political_orientation, country FROM publisher_options WHERE publisher = ?', (publisher,))
        
        if publisher_info:
            # If publisher exists, use the existing political orientation and country
            publisher_political_orientation, country = publisher_info[0]
        else:
            # If publisher does not exist, set as Unknown
            publisher_political_orientation, country = "Unknown", "Unknown"

        self.add_publisher_in_publisher_options(publisher)

        try:
            self.connect()
            query = '''
            UPDATE library
            SET title = ?, transcript = ?, date_published = ?, 
            publisher = ?, reference_image = ?, publisher_political_orientation = ?, 
            country = ?, platform = ?
            WHERE content_id = ?
            '''
            params = (title, transcript, date_published,
                      publisher, reference_image, publisher_political_orientation, country, platform, content_id)
            self.execute_query(query, params)
            self.logger.info(f"Scraped content_id = {content_id}")
        except sqlite3.IntegrityError as e:
            self.logger.error(f"Error scraping content_id = {content_id}. Error: {e}")
        finally:
            self.close()

    def process_content_id(self, content_id):
        """Process the content_id to update the duration in the database."""
        try:
            self.connect()
            # Get the transcript from the database
            transcript_query = "SELECT transcript FROM library WHERE content_id = ?"
            transcript_result = self.query(transcript_query, (content_id,))

            # Ensure that a transcript was found
            if transcript_result:
                # Assuming transcript is the first column
                transcript = transcript_result[0][0]

                # Get the duration processor and analyse the transcript
                duration_processor = get_processor('duration')
                duration_in_minutes = duration_processor.analyse_duration(
                    transcript)

                # summarisation_processor = get_processor('summarisation')
                # summary, sentiment_analysis = summarisation_processor.process_text(
                #     transcript)
                
                summarisation_processor = get_processor('openai_summarisation')
                summary = summarisation_processor.process_text(
                    transcript)
                
                sentiment_analysis = 0

                # Update the duration in the database
                query = '''
                UPDATE library
                SET duration = ?, summary = ?, sentiment_analysis = ?
                WHERE content_id = ?
                '''
                params = (duration_in_minutes, summary,
                          sentiment_analysis, content_id)
                self.execute_query(query, params)
                self.logger.info(f"Processed content_id = {content_id}")
            else:
                print(f"No transcript found for content_id {content_id}")

        except sqlite3.Error as e:
            self.logger.error(f"Error processing content_id = {content_id}. Error: {e}")
        except Exception as e:
            self.logger.error(f"Error processing content_id = {content_id}. Error: {e}")
        finally:
            self.close()

    def fetch_filtered_data(self, filters):
        """Fetch filtered data from the database."""
        base_query = "SELECT * FROM library WHERE 1=1"
        params = []
        query_parts = []

        # Dynamically build the query based on provided filters
        if 'publishers' in filters and filters['publishers']:
            placeholders = ','.join(['?' for _ in filters['publishers']])
            query_parts.append(f"publisher IN ({placeholders})")
            params.extend(filters['publishers'])

        if 'platforms' in filters and filters['platforms']:
            placeholders = ','.join(['?' for _ in filters['platforms']])
            query_parts.append(f"platform IN ({placeholders})")
            params.extend(filters['platforms'])

        if 'countries' in filters and filters['countries']:
            placeholders = ','.join(['?' for _ in filters['countries']])
            query_parts.append(f"country IN ({placeholders})")
            params.extend(filters['countries'])

        if 'macro_topics' in filters and filters['macro_topics']:
            placeholders = ','.join(['?' for _ in filters['macro_topics']])
            query_parts.append(f"macro_topic IN ({placeholders})")
            params.extend(filters['macro_topics'])

        if 'dateAddedRange' in filters and filters['dateAddedRange']:
            query_parts.append("date_added BETWEEN ? AND ?")
            params.extend([filters['dateAddedRange']['start'], filters['dateAddedRange']['end']])

        if 'datePublishedRange' in filters and filters['datePublishedRange']:
            query_parts.append("date_published BETWEEN ? AND ?")
            params.extend([filters['datePublishedRange']['start'], filters['datePublishedRange']['end']])

        if query_parts:
            full_query = f"{base_query} AND {' AND '.join(query_parts)}"
        else:
            full_query = base_query

        # Fetch the filtered data
        return self.execute_query_fetchall(full_query, params)

    def execute_query_fetchall(self, query, params):
        """Execute a query and fetch all results."""
        data_dicts = []
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            columns = [column[0] for column in cursor.description]
            data = cursor.fetchall()
            data_dicts = [dict(zip(columns, row)) for row in data]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            self.close()
        return data_dicts

    def fetch_publisher_options(self):
        """Fetch all publisher options from the database."""
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("SELECT publisher, publisher_political_orientation, country FROM publisher_options")
            columns = ['publisher', 'publisher_political_orientation', 'country']
            data = cursor.fetchall()
            # Create a list of dictionaries, each representing a row from the publisher_options table
            data_dicts = [dict(zip(columns, row)) for row in data]
            return data_dicts
        except Exception as e:
            self.logger.error(f"Error fetching publisher options. Error: {e}")
            return []
        finally:
            self.close()

    def edit_publisher_option(self, publisher, publisher_political_orientation, country):
        """Update a publisher's political orientation and country in the database."""
        try:
            # Update the publisher_options table
            query_publisher_options = '''
            UPDATE publisher_options
            SET publisher_political_orientation = ?, country = ?
            WHERE publisher = ?
            '''
            self.execute_query(query_publisher_options, (publisher_political_orientation, country, publisher))
            self.logger.info(f"Updated publisher options for {publisher}")

            # Update the library table
            query_library = '''
            UPDATE library
            SET publisher_political_orientation = ?, country = ?
            WHERE publisher = ?
            '''
            self.execute_query(query_library, (publisher_political_orientation, country, publisher))
            self.logger.info(f"Updated library entries for publisher {publisher}")
        except sqlite3.Error as e:
            self.logger.error(f"Error updating publisher option for {publisher}. Error: {e}")


# if __name__ == '__main__':
#     db_manager = DBManager('generic_database.db')
#     db_manager.connect()
#     db_manager.create_library_table()
#     db_manager.create_publisher_options_table()
#     db_manager.close()
