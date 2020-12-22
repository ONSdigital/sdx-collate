from app.datastore import fetch_comments

if __name__ == '__main__':
    print('Starting SDX Collate')
    d = fetch_comments()
    print(d)
