import os
import sqlite3

# folder where this script lives, .db files are stored here
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

# three databases: file name, table name, columns and some dummy data
# every table also gets an automatic "id" column
DATABASES = {
    "Students": {
        "file": "students.db",
        "table": "students",
        "columns": [
            ("name", "TEXT"),
            ("email", "TEXT"),
            ("major", "TEXT"),
            ("year", "INTEGER"),
        ],
        "dummy_rows": [
            ("Aino Virtanen", "aino.virtanen@example.com", "Computer Science", 2),
            ("Mikko Korhonen", "mikko.korhonen@example.com", "Data Analytics", 1),
            ("Laura Nieminen", "laura.nieminen@example.com", "Software Engineering", 3),
            ("Juho Makinen", "juho.makinen@example.com", "Industrial Engineering", 2),
            ("Sofia Hamalainen", "sofia.hamalainen@example.com", "Data Analytics", 2),
            ("Eetu Laine", "eetu.laine@example.com", "Computer Science", 4),
            ("Emma Heikkinen", "emma.heikkinen@example.com", "Business Analytics", 1),
            ("Olli Koskinen", "olli.koskinen@example.com", "Software Engineering", 3),
        ],
    },
    "Courses": {
        "file": "courses.db",
        "table": "courses",
        "columns": [
            ("code", "TEXT"),
            ("title", "TEXT"),
            ("credits", "INTEGER"),
            ("teacher", "TEXT"),
        ],
        "dummy_rows": [
            ("CS101", "Introduction to Programming", 5, "Dr. Salo"),
            ("CS201", "Data Structures", 5, "Dr. Lehtonen"),
            ("DA301", "Statistics 1", 5, "Prof. Jarvinen"),
            ("DA302", "Visual Analytics", 5, "Dr. Rantanen"),
            ("SE210", "Requirements Engineering", 5, "Dr. Turunen"),
            ("SE310", "Software Testing", 5, "Dr. Kallio"),
            ("DB220", "Database Systems", 5, "Prof. Mattila"),
            ("RM150", "Risk Management", 3, "Dr. Ojala"),
        ],
    },
    "Library": {
        "file": "library.db",
        "table": "books",
        "columns": [
            ("title", "TEXT"),
            ("author", "TEXT"),
            ("genre", "TEXT"),
            ("copies", "INTEGER"),
        ],
        "dummy_rows": [
            ("The Unknown Soldier", "Vaino Linna", "Novel", 3),
            ("Seven Brothers", "Aleksis Kivi", "Classic", 2),
            ("Clean Code", "Robert C. Martin", "Programming", 4),
            ("Designing Data-Intensive Applications", "Martin Kleppmann", "Databases", 2),
            ("The Pragmatic Programmer", "Andrew Hunt", "Programming", 3),
            ("Storytelling with Data", "Cole Knaflic", "Analytics", 5),
            ("Thinking, Fast and Slow", "Daniel Kahneman", "Psychology", 2),
            ("Moomin Valley in November", "Tove Jansson", "Children", 1),
        ],
    },
}


def open_connection(database_name):
    # open the sqlite file that belongs to this database
    file_path = os.path.join(BASE_FOLDER, DATABASES[database_name]["file"])
    return sqlite3.connect(file_path)


def create_databases():
    # set up every database, create the table and add dummy data if it is empty
    for database_name, config in DATABASES.items():
        column_definitions = ", ".join(
            f"{column_name} {column_type}" for column_name, column_type in config["columns"]
        )
        connection = open_connection(database_name)
        connection.execute(
            f"CREATE TABLE IF NOT EXISTS {config['table']} "
            f"(id INTEGER PRIMARY KEY AUTOINCREMENT, {column_definitions})"
        )

        row_count = connection.execute(f"SELECT COUNT(*) FROM {config['table']}").fetchone()[0]
        if row_count == 0:
            column_names = ", ".join(name for name, _ in config["columns"])
            placeholders = ", ".join("?" for _ in config["columns"])
            connection.executemany(
                f"INSERT INTO {config['table']} ({column_names}) VALUES ({placeholders})",
                config["dummy_rows"],
            )

        connection.commit()  # save the changes to the file
        connection.close()


def show_records(database_name):
    # print every record in a simple table
    config = DATABASES[database_name]
    column_names = ["id"] + [name for name, _ in config["columns"]]

    connection = open_connection(database_name)
    rows = connection.execute(
        f"SELECT {', '.join(column_names)} FROM {config['table']} ORDER BY id"
    ).fetchall()
    connection.close()

    print()
    print(" | ".join(column_names))
    print("-" * 60)
    for row in rows:
        print(" | ".join(str(value) for value in row))
    print(f"({len(rows)} records)")


def ask_for_values(database_name):
    # ask the user for a value for every column
    values = []
    for column_name, _ in DATABASES[database_name]["columns"]:
        values.append(input(f"  {column_name}: ").strip())
    return values


def add_record(database_name):
    config = DATABASES[database_name]
    print("Enter the new record:")
    values = ask_for_values(database_name)

    # the ? placeholders keep user input safe from SQL injection
    column_names = ", ".join(name for name, _ in config["columns"])
    placeholders = ", ".join("?" for _ in config["columns"])
    connection = open_connection(database_name)
    connection.execute(
        f"INSERT INTO {config['table']} ({column_names}) VALUES ({placeholders})", values
    )
    connection.commit()
    connection.close()
    print("Record added.")


def edit_record(database_name):
    config = DATABASES[database_name]
    row_id = input("Id of the record to edit: ").strip()
    print("Enter the new values:")
    values = ask_for_values(database_name)

    # overwrite every column of the record with this id
    assignments = ", ".join(f"{name} = ?" for name, _ in config["columns"])
    connection = open_connection(database_name)
    cursor = connection.execute(
        f"UPDATE {config['table']} SET {assignments} WHERE id = ?", values + [row_id]
    )
    connection.commit()
    connection.close()

    # rowcount tells if a record with that id existed
    if cursor.rowcount == 0:
        print("No record with that id.")
    else:
        print("Record updated.")


def delete_record(database_name):
    config = DATABASES[database_name]
    row_id = input("Id of the record to delete: ").strip()

    connection = open_connection(database_name)
    cursor = connection.execute(f"DELETE FROM {config['table']} WHERE id = ?", (row_id,))
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        print("No record with that id.")
    else:
        print("Record deleted.")


def database_menu(database_name):
    # menu for one database, repeats 
    while True:
        print(f"\n--- {database_name} ---")
        print("1) View records")
        print("2) Add a record")
        print("3) Edit a record")
        print("4) Delete a record")
        print("5) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            show_records(database_name)
        elif choice == "2":
            add_record(database_name)
        elif choice == "3":
            edit_record(database_name)
        elif choice == "4":
            delete_record(database_name)
        elif choice == "5":
            return
        else:
            print("Please type a number from 1 to 5.")


def main():
    create_databases()
    database_names = list(DATABASES.keys())

    # main menu: pick which database to work with
    while True:
        print("\n=== Database Manager ===")
        for number, database_name in enumerate(database_names, start=1):
            print(f"{number}) {database_name}")
        print("0) Quit")
        choice = input("Pick a database: ").strip()

        if choice == "0":
            print("Bye!")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(database_names):
            database_menu(database_names[int(choice) - 1])
        else:
            print("Please pick one of the numbers in the list.")


main()
