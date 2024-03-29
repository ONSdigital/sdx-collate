from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from sdx_gcp.app import get_logger

logger = get_logger()


class InMemoryZip:
    """Class for creating in memory Zip objects using BytesIO."""

    def __init__(self):
        logger.info('Creating in memory zip')
        self.in_memory_zip = BytesIO()

    def append(self, filename_in_zip, file_contents):
        """Appends a file with name filename_in_zip and contents of
        file_contents to the in-memory zip."""
        # Get a handle to the in-memory zip in append mode
        zf = ZipFile(self.in_memory_zip, "a", ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)
        zf.close()
        return self

    def rewind(self):
        """Rewind current file position to the start of in memory file"""
        self.in_memory_zip.seek(0)

    def get(self) -> BytesIO:
        self.rewind()
        return self.in_memory_zip
