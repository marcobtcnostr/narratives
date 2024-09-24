"""
This...
"""

# processor/factory.py

from .duration import Duration
from .summarisation import Summariser
# from .sentiment_analysis import SentimentAnalyser
from .openai_summarisation import OpenAISummariser

def get_processor(type):
    """
    Factory method that returns an instance of a processor based on the provided type.
    """
    if type == 'duration':
        return Duration()
    elif type == 'summarisation':
        return Summariser()
    elif type == 'openai_summarisation':
        return OpenAISummariser()
    # elif type == 'sentiment_analysis':
    #     return SentimentAnalyser()
    else:
        raise ValueError(f"Unknown processor type: {type}")
