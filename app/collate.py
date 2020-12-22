import logging
import time

from datetime import datetime
from structlog import wrap_logger

from app.datastore import fetch_comments
from app.deliver import deliver_comments, DeliveryError
from app.excel import create_excel
from app.in_memory_zip import InMemoryZip

logger = wrap_logger(logging.getLogger(__name__))
RETRY_LIMIT = 5


def collate_comments():
    retry_count = 0
    sleep_time = 1
    while not collate() and retry_count < RETRY_LIMIT:
        logger.info(f"collate failed. Backing off for {sleep_time} seconds")
        time.sleep(sleep_time)
        retry_count = retry_count + 1
        sleep_time * 5


def collate():

    try:
        file_name = get_file_name()
        zip_bytes = create_zip()
        deliver_comments(file_name, zip_bytes)
        return True

    except DeliveryError:
        logger.info("delivery error")
        return False


def get_file_name():
    date_time = datetime.utcnow()
    return f"{date_time.strftime('%Y-%m-%d')}.zip"


def create_zip():

    zip_file = InMemoryZip()

    group_dict = fetch_comments()
    for k, submissions_list in group_dict.items():
        survey_id = k[0:3]
        period = k[4:]

        workbook = create_excel(survey_id, period, submissions_list)
        filename = f"{k}.xls"
        print(f"appending {filename} to zip")
        zip_file.append(filename, workbook)

    return zip_file.get()
