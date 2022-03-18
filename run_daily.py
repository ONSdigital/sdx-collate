import structlog
from datetime import date

from app import cloud_config
from app.collate import create_daily_zip_only


logger = structlog.get_logger()

# change to the desired date before running
chosen_date = date(2022, 3, 17)

if __name__ == '__main__':
    logger.info('Starting SDX-Collate')
    cloud_config()
    zip_file = create_daily_zip_only(chosen_date)
    with open(f"temp/daily_{chosen_date}.zip", "wb") as f:
        f.write(zip_file.getbuffer())
