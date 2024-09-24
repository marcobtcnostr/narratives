"""
This module defines the ContentScraper class, which is designed to scrape content from web pages.
It includes methods to scrape the transcript, date published, and publisher from a given URL.
These functionalities serve as the foundation for extracting relevant information that can be stored in a database or processed further.

Note: The actual implementation of the scraping logic needs to be adapted based on the structure of the target web page.
"""

import logging
import json
from bs4 import BeautifulSoup
from scraper.utils.scraping_utils import safe_request, standardize_date, clean_text


class BBCScraper:
    """
    This class is designed to scrape content from BBC web pages.
    """

    def __init__(self, content_id):
        self.content_id = content_id
        self._soup = None  # Initialize a variable to cache the BeautifulSoup object
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_soup(self):
        """Use safe_request utility to make an HTTP request and return a BeautifulSoup object."""
        if not self._soup:  # Check if the soup has already been fetched
            response = safe_request(self.content_id)
            if response:
                self._soup = BeautifulSoup(
                    response.text, 'html.parser')  # Cache the soup object
            else:
                self.logger.error(f"Failed to retrieve content from {self.content_id}")
        return self._soup  # Return the cached soup object

    def scrape_title(self):
        """Scrape the title from the content_id."""
        soup = self.get_soup()
        if soup:
            title_tag = soup.find('meta', property='og:title')
            if title_tag:
                return title_tag.get('content')
            else:
                self.logger.warning("Title tag not found.")
        return None

    def scrape_transcript(self):
        """Scrape the transcript from the content_id."""
        soup = self.get_soup()
        if soup:

            div_elements = soup.find_all(
                'div', attrs={'data-component': 'text-block'})
            texts = []
            for div_element in div_elements:
                text = div_element.get_text(strip=True)
                texts.append(text)

            if texts:
                transcript_tmp = ' '.join(texts)
                transcript = clean_text(transcript_tmp)

                return transcript

            else:
                self.logger.warning("Transcript div not found.")
        return None

    def scrape_date_published(self):
        """Scrape the date published from the content_id."""
        soup = self.get_soup()
        if soup:
            script_tag = soup.find('script', type='application/ld+json')
            if script_tag:
                try:
                    # Attempt to parse the JSON data within the <script> tag
                    json_data = json.loads(script_tag.string)

                    # Handle cases where JSON data is a list or directly a dictionary
                    if isinstance(json_data, list):
                        # Assuming the first element is relevant
                        json_data = json_data[0]

                    # Extract and format the datePublished
                    if 'datePublished' in json_data:
                        date_published_str = json_data['dateModified']
                        date_published = standardize_date(date_published_str)
                        return date_published

                except json.JSONDecodeError:
                    self.logger.error("Error decoding JSON from script tag.")
            else:
                self.logger.warning(
                    "Script tag with type 'application/ld+json' not found.")
        return None

    def scrape_publisher(self):
        """Scrape the publisher from the content_id."""
        soup = self.get_soup()
        if soup:
            publisher_tag = soup.find('meta', property='og:site_name')
            if publisher_tag:
                return publisher_tag.get('content')
            else:
                self.logger.warning("Publisher tag not found.")
        return None


    def scrape_reference_image(self):
        """Scrape the reference image from the content_id."""
        soup = self.get_soup()
        if soup:
            reference_image_tag = soup.find('meta', property='og:image')
            if reference_image_tag:
                return reference_image_tag.get('content')
            else:
                self.logger.warning("Reference image tag not found.")
        return None
