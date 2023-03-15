import csv
import json


def convert_file(csv_file, json_file, model):
    result = []
    with open(csv_file, "r", encoding="utf-8") as csv_f:
        for row in csv.DictReader(csv_f):
            del row['id']
            if 'price' in row:
                row['price'] = int(row['price'])
            if 'is_published' in row:
                if 'is_published' == "TRUE":
                    row['is_published'] = True
                else:
                    row['is_published'] = False

            result.append({'model': model, 'fields': row})

    with open(json_file, "w", encoding="utf-8") as json_f:
        json_f.write(json.dumps(result, indent=4, ensure_ascii=False))

convert_file('ad.csv', 'ad.json', 'ads.announcement')
convert_file('category.csv', 'category.json', 'ads.category')
convert_file('location.csv', 'location.json', 'ads.location')
convert_file('user.csv', 'user.json', 'ads.user')