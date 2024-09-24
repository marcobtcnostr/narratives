"""
This ...
"""

from scraper.sources.bbc_scraper import BBCScraper
from scraper.sources.cnbc_scraper import CNBCScraper
from scraper.sources.youtube_scraper import YouTubeScraper
# from scraper.sources.wikipedia_scraper import WikipediaScraper

def get_scraper(content_id: str):
    if "bbc.co.uk" in content_id:
        return BBCScraper(content_id)
    elif "cnbc.com" in content_id:
        return CNBCScraper(content_id)
    elif "youtube.com" in content_id:
        return YouTubeScraper(content_id)
    # elif "wikipedia.org" in content_id:
    #     return WikipediaScraper(content_id)
    else:
        raise ValueError("Unsupported URL")
