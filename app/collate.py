from app.excel import create_excel
from app.in_memory_zip import InMemoryZip


def collate_comments(submission_list):

    in_memory_zip = InMemoryZip()
    filename, workbook = create_excel("134", "2019", submission_list)
    in_memory_zip.append(filename, workbook)
    return in_memory_zip.get_filenames()
