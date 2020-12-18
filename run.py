from app.datastore_reader import fetch_all_comments

if __name__ == '__main__':
    print('Starting SDX Collate')
    d = fetch_all_comments()
    print(d)
