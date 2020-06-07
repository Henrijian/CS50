import csv
import sys
import ntpath
import sqlite3

DB_NAME = 'students.db'
DB_TABLE_NAME = 'students'
DB_FIRST_NAME_COL = 'first'
DB_MIDDLE_NAME_COL = 'middle'
DB_LAST_NAME_COL = 'last'
DB_HOUSE_COL = 'house'
DB_BIRTH_COL = 'birth'
CSV_NAME_COL = 'name'
CSV_HOUSE_COL = 'house'
CSV_BIRTH_COL = 'birth'


def main():
    # Check arguments from user
    if len(sys.argv) != 2:
        print(f'Usage: python {path_leaf(sys.argv[0])} characters.csv')
        return
    # Connect with database
    conn = sqlite3.connect(DB_NAME)
    try:
        # Initialize database
        conn.execute(f'DELETE FROM {DB_TABLE_NAME}')
        # Load characters csv file into csv reader
        characters_path = sys.argv[1]
        with open(characters_path, 'r', newline='') as characters_file:
            reader = csv.DictReader(characters_file, delimiter=',')
            for row in reader:
                # Parse each line of csv file
                name_tokens = row[CSV_NAME_COL].split(' ')
                if len(name_tokens) == 3:
                    first_name = name_tokens[0]
                    middle_name = name_tokens[1]
                    last_name = name_tokens[2]
                elif len(name_tokens) == 2:
                    first_name = name_tokens[0]
                    middle_name = None
                    last_name = name_tokens[1]
                else:
                    continue
                house = row[CSV_HOUSE_COL]
                birth = row[CSV_BIRTH_COL]
                # Store parsed info into database
                conn.execute(f'''INSERT INTO {DB_TABLE_NAME} 
                            ({DB_FIRST_NAME_COL}, {DB_MIDDLE_NAME_COL}, {DB_LAST_NAME_COL},
                            {DB_HOUSE_COL}, {DB_BIRTH_COL}) VALUES(?, ?, ?, ?, ?)''',
                             (first_name, middle_name, last_name, house, birth))
    finally:
        conn.commit()
        conn.close()


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


if __name__ == '__main__':
    main()