import structlog
from google.cloud import secretmanager

logger = structlog.get_logger()


def get_secret(project_id, secret_id):
    logger.info('Getting secrets')

    version_id = 'latest'

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(request={"name": name})

    payload = response.payload.data.decode("UTF-8")
    return payload
