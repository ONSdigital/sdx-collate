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
    Orchestrates the required steps to process all comments stored within Datastore and save them in the
    sdx-outputs bucket.
    The steps include:
        - Generating filename (Current date)
        - Creating the in memory zip, fetch comments and generate excel file
        - Calls SDX-Deliver endpoint to store
    and are dependent on the survey and type of the submission.
    """
    try:
        bind_contextvars(app="SDX-Collate")
        file_name = generate_filename()
        zip_bytes = create_zip()
        deliver_comments(file_name, zip_bytes)
    except DeliveryError:
        logger.error("Delivery error")


def generate_filename():
    """
    Generates filename based on current date.
    """
    logger.info('Getting filename')
    date_time = datetime.utcnow()
    return f"{date_time.strftime('%Y-%m-%d')}.zip"


def create_zip():
    """
    Generates an Excel file using the comments gathered from datastore and stores within an instance of InMemoryZip
    """
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
