import structlog

from datetime import datetime
from structlog.contextvars import bind_contextvars
from app.datastore_connect import fetch_comments
from app.deliver import deliver_comments, DeliveryError
from app.excel import create_excel
from app.in_memory_zip import InMemoryZip

logger = structlog.get_logger()


def collate_comments():
    try:
        bind_contextvars(app="SDX-Worker")
        file_name = get_file_name()
        zip_bytes = create_zip()
        deliver_comments(file_name, zip_bytes)

    except DeliveryError:
        logger.error("Delivery error")


def get_file_name():
    logger.info('Getting filename')
    date_time = datetime.utcnow()
    return f"{date_time.strftime('%Y-%m-%d')}.zip"


def create_zip():
    logger.info('Creating zip file')
    zip_file = InMemoryZip()
    group_dict = fetch_comments()
    for k, submissions_list in group_dict.items():
        survey_id = k[0:3]
        period = k[4:]

        workbook = create_excel(survey_id, period, submissions_list)
        filename = f"{k}.xls"
        logger.info(f"Appending {filename} to zip")
        zip_file.append(filename, workbook)

    return zip_file.get()
