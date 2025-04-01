import json

def data_set(database):
    pass_count = {}
    for id, schools in database.items():
        for school in schools:
            if id == 'pass_count':
                pass
            else:
                if school not in pass_count:
                    pass_count[f'{school}'] = [0]
                pass_count[f'{school}'].append(id)
                pass_count[f'{school}'][0] += 1

    database['pass_count'] = pass_count

    with open('For_Fun/json/passcount.json', 'w', encoding='utf-8') as f:
        json.dump(database['pass_count'], f, ensure_ascii=False, indent=2)

    del database['pass_count']
    with open('For_Fun/json/database.json', 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    with open('For_Fun/json/database.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
    data_set(database)
