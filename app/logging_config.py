import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                f"{log_dir}/qa_app.log",
                maxBytes=10485760,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler(sys.stdout)
        ]
    )