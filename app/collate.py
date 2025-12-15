from datetime import datetime, date, timedelta
from io import BytesIO
from typing import IO

from sdx_gcp.app import get_logger

from app.services.reader import fetch_comment_kinds, fetch_data_for_kind, fetch_data_for_survey
from app.services.decrypter import decrypt_comment
from app.services.deliver import deliver_comments
from app.services.writer import create_excel
from app.services.zip import InMemoryZip
from app.submission import Submission

logger = get_logger()


def collate_comments():
    """
    Generates a zip of Excel files reporting the significant comments and associated metadata.

    The comments are read from Datastore, written to Excel files, and then posted to sdx-deliver.
    """
    try:
        file_name = generate_zip_filename()
        today = date.today()
        zip_bytes = create_full_zip(today)
        deliver_comments(file_name, zip_bytes)
    except Exception as e:
        logger.error("Delivery error", error=str(e))


def generate_zip_filename() -> str:
    """
    Generates the filename based on current date and time.
    """
    logger.info('Getting filename')
    date_time = datetime.utcnow()
    return f"{date_time.strftime('%Y-%m-%d_%H-%M-%S')}.zip"


def create_full_zip(day: date) -> IO[bytes]:
    """
    Creates a zipfile containing both the 90 days files and the daily files.

    The 90 days files each contain the last 90 days worth of comments for a single period of a single survey.
    The daily files only contain the last days worth of comments but may contain multiple periods for each survey.
    """
    logger.info('Creating zip file')
    zip_file = InMemoryZip()

    append_90_days_files(zip_file, day)

    # On a Monday we need to get the daily files for Friday, Saturday and Sunday. Else just get the day before.
    if day.strftime('%A') == 'Monday':
        friday = day - timedelta(3)
        saturday = day - timedelta(2)
        sunday = day - timedelta(1)
        days = [friday, saturday, sunday]
    else:
        yesterday = day - timedelta(1)
        days = [yesterday]

    for d in days:
        append_daily_files(zip_file, d)

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


def append_90_days_files(zip_file: InMemoryZip, today: date):
    """
    Appends files for each distinct survey and period containing the last 90 days of comments
    Each file is named <survey_id>_<period>.xlsx e.g. 009_2105.xlsx.
    """
    end_date = to_datetime(today)
    ninety_days_ago = to_datetime(end_date) - timedelta(90)
    kinds = fetch_comment_kinds()
    for k in kinds:
        survey_id, _, period = k.partition('_')
        # get the list of encrypted data for this kind
        encrypted_data_list = fetch_data_for_kind(k, start_date=ninety_days_ago, end_date=end_date)
        # decrypt the data in the list and convert to Submission
        submission_list = [Submission(period, decrypt_comment(c)) for c in encrypted_data_list]
        # create the workbook
        workbook, _ = create_excel(survey_id, submission_list)
        filename = f"{k}.xlsx"
        logger.info(f"Appending {filename} to zip")
        zip_file.append(filename, workbook)


def append_daily_files(zip_file: InMemoryZip, chosen_day: date):
    """
    Appends files for each distinct survey containing the comments
    for all periods recorded on the 'chosen_day' given.

    Each file is named <survey_id>-daily-<chosen_day>.xlsx e.g. 009_daily_2022-03-16.xlsx.
    """
    start_date = to_datetime(chosen_day)
    end_date = start_date + timedelta(1)
    kinds = fetch_comment_kinds()
    daily_dict = get_daily_dict(kinds)
    for survey_id, period_list in daily_dict.items():
        encrypted_data_dict = fetch_data_for_survey(survey_id,
                                                    period_list,
                                                    start_date=start_date,
                                                    end_date=end_date)
        submission_list = []
        for period, encrypted_data_list in encrypted_data_dict.items():
            # decrypt the data in the list and convert to Submission
            sub_list_for_period = [Submission(period, decrypt_comment(c)) for c in encrypted_data_list]
            submission_list.extend(sub_list_for_period)

        # create the workbook
        workbook, count = create_excel(survey_id, submission_list)
        if count > 0:
            filename = f"{survey_id}_daily_{chosen_day}.xlsx"
            logger.info(f"Appending {filename} to zip")
            zip_file.append(filename, workbook)


def get_daily_dict(kinds: list[str]) -> dict[str, list[str]]:
    daily_dict = {}
    for k in kinds:
        survey_id, _, period = k.partition('_')
        if survey_id not in daily_dict:
            daily_dict[survey_id] = []
        daily_dict[survey_id].append(period)

    return daily_dict


def to_datetime(d: date) -> datetime:
    return datetime(d.year, d.month, d.day)
