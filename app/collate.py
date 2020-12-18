from app.datastore_reader import fetch_all_comments
from app.excel import create_excel
from app.in_memory_zip import InMemoryZip


def collate_comments():

    in_memory_zip = InMemoryZip()

    group_dict = fetch_all_comments()
    for k, submissions_list in group_dict.items():
        survey_id = k[0:3]
        period = k[4:]

        workbook = create_excel(survey_id, period, submissions_list)
        filename = f"{k}.xls"
        print(f"appending {filename} to zip")
        in_memory_zip.append(filename, workbook)

    return in_memory_zip.get_filenames()
