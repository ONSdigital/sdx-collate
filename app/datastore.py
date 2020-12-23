import json
from datetime import date, datetime

from google.cloud import datastore

from app import PROJECT
from app.decrypt import decrypt_comment

datastore_client = datastore.Client(project=PROJECT)


def fetch_comments() -> dict:

    d = date.today()
    today = datetime(d.year, d.month, d.day)

    query = datastore_client.query(kind='Comment')
    query.add_filter("created", "<", today)
    results = query.fetch()

    group_dict = {}
    for entity in results:
        key = f"{entity['survey_id']}_{entity['period']}"
        value = json.loads(decrypt_comment(entity['encrypted_data']))
        if key in group_dict.keys():
            group_dict[key].append(value)
        else:
            group_dict[key] = [value]

    return group_dict
