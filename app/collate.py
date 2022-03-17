from datetime import datetime, date, timedelta
from io import BytesIO
from typing import List, Dict, IO

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
    Generates a zip of Excel files reporting the significant comments and associated metadata.

    The comments are read from Datastore, written to Excel files, and then posted to sdx-deliver.
    """
    try:
        bind_contextvars(app="SDX-Collate")
        file_name = generate_zip_filename()
        zip_bytes = create_full_zip()
        deliver_comments(file_name, zip_bytes)
    except DeliveryError:
        logger.error("Delivery error")


def generate_zip_filename() -> str:
    """
    Generates the filename based on current date and time.
    """
    logger.info('Getting filename')
    date_time = datetime.utcnow()
    return f"{date_time.strftime('%Y-%m-%d_%H-%M-%S')}.zip"


def create_full_zip() -> IO[bytes]:
    """
    Creates a zipfile containing both the 90 days files and the daily files.

    The 90 days files each contain the last 90 days worth of comments for a single period of a single survey.
    The daily files only contain the last days worth of comments but may contain multiple periods for each survey.
    """
    logger.info('Creating zip file')
    zip_file = InMemoryZip()
    today = date.today()
    append_90_days_files(zip_file, today)
    yesterday = today - timedelta(1)
    append_daily_files(zip_file, yesterday)
    return zip_file.get()


def create_daily_zip_only(day: date) -> BytesIO:
    """
    Creates a zipfile containing only comments received on the provided 'day'
    Each file represents a single survey but may contain comments for multiple periods
    """
    logger.info('Creating zip file')
    zip_file = InMemoryZip()
    append_daily_files(zip_file, day)
    return zip_file.get()


def append_90_days_files(zip_file: InMemoryZip, end_date: date):
    # set the cutoff date as 90 days prior to end_date
    ninety_days = to_datetime(end_date) - timedelta(90)
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


def append_daily_files(zip_file: InMemoryZip, chosen_date: date):
    kinds = fetch_comment_kinds()
    daily_dict = get_daily_dict(kinds)
    day = to_datetime(chosen_date)
    for survey_id, period_list in daily_dict.items():
        encrypted_data_dict = fetch_data_for_survey(survey_id, period_list, op='=', cutoff_date=day)
        submission_list = []
        for period, encrypted_data_list in encrypted_data_dict.items():
            # decrypt the data in the list and convert to Submission
            sub_list_for_period = [Submission(period, decrypt_comment(c)) for c in encrypted_data_list]
            submission_list.extend(sub_list_for_period)

        # create the workbook
        workbook = create_excel(survey_id, submission_list)
        filename = f"{survey_id}-daily-{chosen_date}.xlsx"
        logger.info(f"Appending {filename} to zip")
        zip_file.append(filename, workbook)


def get_daily_dict(kinds: List[str]) -> Dict[str, List[str]]:
    daily_dict = {}
    for k in kinds:
        survey_id, _, period = k.partition('_')
        if survey_id not in daily_dict:
            daily_dict[survey_id] = []
        daily_dict[survey_id].append(period)

    return daily_dict


def to_datetime(d: date) -> datetime:
    return datetime(d.year, d.month, d.day)
