import os
import sys
import logging
from alembic.config import Config
from alembic import command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    try:
        alembic_ini_path = os.path.join(os.path.dirname(__file__), '..', 'alembic.ini')
        alembic_cfg = Config(alembic_ini_path)
        
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrations applied successfully")
    except Exception as e:
        logger.error(f"Failed to apply migrations: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()