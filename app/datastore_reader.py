from google.cloud import datastore

from app import PROJECT

datastore_client = datastore.Client(project=PROJECT)


def fetch_all_comments() -> dict:

    query = datastore_client.query(kind='Comment')
    results = query.fetch()

    group_dict = {}
    for entity in results:
        key = f"{entity['survey_id']}_{entity['period']}"
        value = decrypt(entity['encrypted_data'])
        if key in group_dict.keys():
            group_dict[key].append(value)
        else:
            group_dict[key] = [value]

    return group_dict


def decrypt(encrypted_data):
    return encrypted_data
