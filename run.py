import structlog

from app import get_config
from app.collate import collate_comments

logger = structlog.get_logger()

if __name__ == '__main__':
    get_config()
    logger.info('Starting SDX-Collate')
    collate_comments()
