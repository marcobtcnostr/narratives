"""
This ...
"""

# scraper\utils\scraping_utils.py

import requests
from requests.exceptions import RequestException
from dateutil import parser
import re


def safe_request(url, max_retries=3, timeout=5):
    """Attempt to make a request to the URL, with retries and timeout."""
    for _ in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raise an error for bad statuses
            return response
        except RequestException as e:
            print(f"Request failed: {e}")
    return None  # Indicate failure after retries


def standardize_date(date_string, output_format='%Y-%m-%d %H:%M:%S'):
    """Parse a date string into a standardized UTC format."""
    try:
        # The parser.parse function automatically detects and parses the date string.
        date = parser.parse(date_string)
        
        # Assuming the parsed date is already in UTC. If not, you will need to convert it to UTC.
        return date.strftime(output_format)
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return None

def clean_text(text):
    """
    Cleans the input text by removing non-ASCII characters and replacing smart quotes
    with their ASCII equivalents.
    """
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Replace smart quotes and other typographically specific characters with ASCII equivalents
    replacements = {
        u"\u2018": "'",  # Left single quotation mark
        u"\u2019": "'",  # Right single quotation mark
        u"\u201c": '"',  # Left double quotation mark
        u"\u201d": '"',  # Right double quotation mark
        u"\u2013": '-',  # En dash
        u"\u2014": '-',  # Em dash
        # Add any other character replacements here
    }
    
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    
    return text

