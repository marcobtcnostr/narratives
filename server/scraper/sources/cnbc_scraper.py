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


class CNBCScraper:
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

            article_body_tag = soup.find('div', class_='ArticleBody-articleBody')

            if article_body_tag:
                transcript_tmp = article_body_tag.get_text(strip=True)
                transcript = clean_text(transcript_tmp)
                return transcript
            else:
                self.logger.warning("articleBody not found.")
        return None

    def scrape_date_published(self):
        """Scrape the date published from the content_id."""
        soup = self.get_soup()
        if soup:
            date_published_tag = soup.find('meta', itemprop='dateCreated')
            if date_published_tag:
                date_published_str = date_published_tag.get('content')
                date_published = standardize_date(date_published_str)
                return date_published
            else:
                self.logger.warning("Date published tag not found.")
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
