from datetime import datetime, date, timedelta
from typing import List, Dict

import structlog
from structlog.contextvars import bind_contextvars

from app.datastore_connect import fetch_comment_kinds, fetch_data_for_kind, fetch_data_for_survey
from app.decrypt import decrypt_comment
from app.deliver import deliver_comments, DeliveryError
from app.excel import create_excel
from app.in_memory_zip import InMemoryZip
from app.submission import Submission

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
    return f"{date_time.strftime('%Y-%m-%d_%H-%M-%S')}.zip"


def create_zip():
    """
    Generates an Excel file using the comments gathered from datastore and stores within an instance of InMemoryZip
    """
    logger.info('Creating zip file')
    zip_file = InMemoryZip()

    # Standard comments
    # set the cutoff date as 90 days prior to today
    ninety_days = get_datetime(90)
    kinds = fetch_comment_kinds()
    for k in kinds:
        survey_id, _, period = k.partition('_')
        # get the list of encrypted data for this kind
        encrypted_data_list = fetch_data_for_kind(k, op='>=', cutoff_date=ninety_days)
        # decrypt the data in the list and convert to Submission
        submission_list = [Submission(period, decrypt_comment(c)) for c in encrypted_data_list]
        # create the workbook
        workbook = create_excel(survey_id, submission_list)
        filename = f"{k}.xlsx"
        logger.info(f"Appending {filename} to zip")
        zip_file.append(filename, workbook)

    # daily comments
    daily_dict = get_daily_dict(kinds)
    # set the search date as yesterday
    yesterday = get_datetime(1)
    for survey_id, period_list in daily_dict.items():
        encrypted_data_dict = fetch_data_for_survey(survey_id, period_list, op='=', cutoff_date=yesterday)
        submission_list = []
        for period, encrypted_data_list in encrypted_data_dict.items():
            # decrypt the data in the list and convert to Submission
            sub_list_for_period = [Submission(period, decrypt_comment(c)) for c in encrypted_data_list]
            submission_list.extend(sub_list_for_period)

        # create the workbook
        workbook = create_excel(survey_id, submission_list)
        filename = f"{survey_id}-daily.xlsx"
        logger.info(f"Appending {filename} to zip")
        zip_file.append(filename, workbook)

    return zip_file.get()


def get_daily_dict(kinds: List[str]) -> Dict:
    daily_dict = {}
    for k in kinds:
        survey_id, _, period = k.partition('_')
        if survey_id not in daily_dict:
            daily_dict[survey_id] = []
        daily_dict[survey_id].append(period)

    return daily_dict


def get_datetime(no_days_previous: int):
    d = date.today()
    today = datetime(d.year, d.month, d.day)
    return today - timedelta(no_days_previous)
