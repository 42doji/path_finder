import csv


file_paths = ['area_category.csv',  'area_map.csv',  'area_struct.csv',  'csv_reader.py']

def read_print():
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            read_file = csv.reader(file)
            for row in read_file:
                print(row)

if __name__ == "__main__":
    read_print()
