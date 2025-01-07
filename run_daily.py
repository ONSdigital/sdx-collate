import structlog
from datetime import date

from app import cloud_config
from app.collate import create_daily_zip_only, create_full_zip

logger = structlog.get_logger()

# change to the desired date before running
chosen_day = date(2024, 7, 26)

# create full zip or just daily
full_zip = True

if __name__ == '__main__':
    logger.info('Starting SDX-Collate')
    cloud_config()
    zip_file = create_full_zip(chosen_day) if full_zip else create_daily_zip_only(chosen_day)
    with open(f"temp/daily_{chosen_day}.zip", "wb") as f:
        f.write(zip_file.getbuffer())
