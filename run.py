import structlog

from app import cloud_config
from app.collate import collate_comments

logger = structlog.get_logger()

if __name__ == '__main__':
    logger.info('Starting SDX-Collate')
    cloud_config()
    collate_comments()
