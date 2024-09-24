# tests/test_bbc_scraper.py

import pytest
import requests_mock
from scraper.sources.bbc_scraper import BBCScraper

@pytest.fixture
def bbc_scraper():
    """Fixture to create a BBCScraper instance with a sample URL."""
    return BBCScraper("https://www.bbc.co.uk/news/business-68225189")

@pytest.fixture
def mock_response():
    """Fixture to provide a mocked HTML response of a BBC article."""
    with requests_mock.Mocker() as m:
        m.get("https://www.bbc.co.uk/news/business-68225189", text="<html><head>"
            "<meta property='og:title' content='House price rises highest for a year in January, Halifax says'>"
            "</head><body>"
            "<div id='transcript'>This is a test transcript.</div>"
            "<meta property='datePublished' content='2024-02-11T10:00:00Z'>"
            "<meta name='publisher' content='BBC News'>"
            "</body></html>")
        yield m

def test_scrape_title(bbc_scraper, mock_response):
    """Test the scraping of the title."""
    title = bbc_scraper.scrape_title()
    assert title == "House price rises highest for a year in January, Halifax says"

# def test_scrape_transcript(bbc_scraper, mock_response):
#     """Test the scraping of the transcript."""
#     transcript = bbc_scraper.scrape_transcript()
#     assert transcript == "This is a test transcript."

# def test_scrape_date_published(bbc_scraper, mock_response):
#     """Test the scraping of the date published."""
#     date_published = bbc_scraper.scrape_date_published()
#     assert date_published == "2024-02-11 17:47:56"

# def test_scrape_publisher(bbc_scraper, mock_response):
#     """Test the scraping of the publisher."""
#     publisher = bbc_scraper.scrape_publisher()
#     assert publisher == "BBC News"
