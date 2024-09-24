import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(environment):
    """
    Setup logging based on the environment ('development' or 'production').
    In 'development', logs go to both console and file.
    In 'production', logs go only to console.
    """
    
    # Configure the basic logging: This setup affects the root logger.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Define loggers and their configurations
    loggers_info = {
        'httpx': {'filename': 'logs/httpx.log', 'level': logging.INFO},
        'openai': {'filename': 'logs/openai.log', 'level': logging.INFO},
        'DBManager': {'filename': 'logs/DBManager.log', 'level': logging.INFO},
        'Summariser': {'filename': 'logs/Summariser.log', 'level': logging.INFO},
        'OpenAISummariser': {'filename': 'logs/OpenAISummariser.log', 'level': logging.INFO},
        'BBCScraper': {'filename': 'logs/BBCScraper.log', 'level': logging.INFO},
        'CNBCScraper': {'filename': 'logs/CNBCScraper.log', 'level': logging.INFO},
        'YouTubeScraper': {'filename': 'logs/YouTubeScraper.log', 'level': logging.INFO},
        'OpenAIChatbot': {'filename': 'logs/OpenAIChatbot.log', 'level': logging.INFO}
    }

    is_production = environment == 'production'

    for logger_name, info in loggers_info.items():
        logger = logging.getLogger(logger_name)

        if not is_production:
            # In development mode, log to both file and console
            if not os.path.exists('logs'):
                os.makedirs('logs')  # Create logs directory if it doesn't exist

            file_handler = RotatingFileHandler(info['filename'], maxBytes=1048576, backupCount=5, delay=True)
            file_handler.setLevel(info['level'])
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(file_handler)

        # Always log to console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(info['level'])
        stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(stream_handler)

        logger.setLevel(info['level'])
        logger.propagate = False  # No need to propagate to the root logger in this case
