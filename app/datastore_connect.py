import structlog

from datetime import date, datetime
from app import CONFIG
from app.decrypt import decrypt_comment

logger = structlog.get_logger()


def fetch_comments() -> dict:
    try:
        logger.info('Fetching comments from Datastore')
        d = date.today()
        today = datetime(d.year, d.month, d.day)
        query = CONFIG.DATASTORE_CLIENT.query(kind='Comment')
        query.add_filter("created", "<", str(today))
        results = query.fetch()

        logger.info('Sorting query results')
        group_dict = {}
        for entity in results:
            key = f"{entity['survey_id']}_{entity['period']}"
            value = decrypt_comment(entity['encrypted_data'])
            if key in group_dict.keys():
                group_dict[key].append(value)
            else:
                group_dict[key] = [value]

        return group_dict

    except Exception as e:
        logger.error(f'Datastore: {e}')
