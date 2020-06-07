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


def main():
    # Check arguments from user
    if len(sys.argv) != 2:
        print(f'Usage: python {path_leaf(sys.argv[0])} house_name')
        return
    # Connect with database
    conn = sqlite3.connect(DB_NAME)
    try:
        # Get house name from argument
        house_name = sys.argv[1]
        # Get info from database by house name
        query_statement = f'''SELECT {DB_FIRST_NAME_COL}, {DB_MIDDLE_NAME_COL}, {DB_LAST_NAME_COL}, {DB_BIRTH_COL} 
                            FROM {DB_TABLE_NAME} WHERE {DB_HOUSE_COL}=? 
                            ORDER BY {DB_LAST_NAME_COL}, {DB_FIRST_NAME_COL}'''
        cur = conn.cursor()
        cur.execute(query_statement, (house_name,))
        rows = cur.fetchall()
        # Show info
        for row in rows:
            first_name = row[0]
            middle_name = row[1]
            last_name = row[2]
            birth_year = row[3]
            if middle_name:
                print(f'{first_name} {middle_name} {last_name}, born {birth_year}')
            else:
                print(f'{first_name} {last_name}, born {birth_year}')
    finally:
        conn.close()


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


if __name__ == '__main__':
    main()