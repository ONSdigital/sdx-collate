import logging

from datetime import datetime
from structlog import wrap_logger

from app.datastore import fetch_comments
from app.deliver import deliver_comments, DeliveryError
from app.excel import create_excel
from app.in_memory_zip import InMemoryZip

logger = wrap_logger(logging.getLogger(__name__))


def collate_comments():
    try:
        file_name = get_file_name()
        zip_bytes = create_zip()
        deliver_comments(file_name, zip_bytes)

    except DeliveryError:
        logger.info("delivery error")


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
