import pprint

import structlog

from datetime import datetime
from structlog.contextvars import bind_contextvars
from app.datastore_connect import fetch_comments
from app.deliver import deliver_comments, DeliveryError
from app.excel import create_excel
from app.in_memory_zip import InMemoryZip

logger = structlog.get_logger()


def collate_comments():
    """
    This method brings together (calls) the main functionality of sdx-collate
    """
    bind_contextvars(app="SDX-Collate")
    file_name = generate_filename()
    zip_bytes = create_zip()
    deliver_comments(file_name, zip_bytes)


def generate_filename():
    logger.info('Getting filename')
    date_time = datetime.utcnow()
    return f"{date_time.strftime('%Y-%m-%d')}.zip"


def create_zip():
    logger.info('Creating zip file')
    zip_file = InMemoryZip()
    group_dict = fetch_comments()
    for survey_period, comment_list in group_dict.items():
        survey_id = survey_period[0:3]
        period = survey_period[4:]

        workbook = create_excel(survey_id, period, comment_list)
        filename = f"{survey_period}.xls"
        logger.info(f"Appending {filename} to zip")
        zip_file.append(filename, workbook)

    return zip_file.get()
