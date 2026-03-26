"""Library management program using Python and MySQL."""

import sys
import time

import mysql.connector as my


DB_CONFIG = {
    "host": "localhost",
    "user": "rachkanc",
    "password": "rach123",
}
DB_NAME = "library"


def connect_server():
    """Connect to MySQL server."""
    try:
        connection = my.connect(**DB_CONFIG)
    except my.Error as exc:
        print(f"Unable to connect to MySQL: {exc}")
        sys.exit(1)

    if connection.is_connected():
        print("\t\t****WELCOME TO LIBRARY****")
        print("\t\t\t\t -MADE BY RACHIT")
        return connection

    print("Connection not built")
    sys.exit(1)


def setup_database(connection, cursor):
    """Create database and tables if they do not exist."""
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS book (
            isbn VARCHAR(20) PRIMARY KEY,
            book_title VARCHAR(100),
            author_name VARCHAR(100),
            publisher VARCHAR(100),
            publication_year INT,
            book_type VARCHAR(30),
            language VARCHAR(30)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS issue (
            isbn VARCHAR(20) PRIMARY KEY,
            book_title VARCHAR(100),
            issuer_name VARCHAR(100),
            date_of_issue VARCHAR(10),
            contact_no BIGINT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS returns (
            isbn VARCHAR(20) PRIMARY KEY,
            book_title VARCHAR(100),
            issuer_name VARCHAR(100),
            date_of_issue VARCHAR(10),
            date_of_return VARCHAR(10),
            fine FLOAT,
            contact_no BIGINT
        )
        """
    )
    connection.commit()


def pause():
    time.sleep(1)


def fetch_book_by_isbn(cursor, isbn):
    cursor.execute("SELECT * FROM book WHERE isbn = %s", (isbn,))
    return cursor.fetchone()


def print_rows(rows):
    if not rows:
        print("No records found.")
        return

    for row in rows:
        print(row)


def search_books(cursor):
    while True:
        print("__SEARCH BOOKS__")
        print('ENTER "1" TO SORT BOOKS A-Z')
        print('ENTER "2" TO SORT BOOKS Z-A')
        print('ENTER "3" TO GROUP BY BOOK TYPE')
        print('ENTER "4" TO FILTER BY PUBLICATION YEAR RANGE')
        print('ENTER "5" TO SEARCH BY ISBN')
        print('ENTER "6" TO SEARCH BY BOOK TITLE')
        print('ENTER "7" TO SEARCH BY AUTHOR')
        print('ENTER "8" TO SEARCH BY PUBLISHER')
        print('ENTER "9" TO SEARCH BY PUBLICATION YEAR')
        print('ENTER "10" TO SEARCH BY BOOK TYPE')
        print('ENTER "11" TO SEARCH BY LANGUAGE')
        print('ENTER "0" TO GO BACK')

        try:
            choice = int(input("ENTER YOUR CHOICE (0-11): "))
        except ValueError:
            print("ENTER A VALID NUMBER !!")
            continue

        if choice == 0:
            return
        if choice == 1:
            cursor.execute("SELECT * FROM book ORDER BY book_title")
        elif choice == 2:
            cursor.execute("SELECT * FROM book ORDER BY book_title DESC")
        elif choice == 3:
            cursor.execute("SELECT * FROM book ORDER BY book_type, book_title")
        elif choice == 4:
            print("__SELECT RANGE OF YEAR__")
            print('ENTER "1" TO SHOW BOOKS PUBLISHED BEFORE YEAR 2000')
            print('ENTER "2" TO SHOW BOOKS PUBLISHED BETWEEN YEAR 2000 TO 2010')
            print('ENTER "3" TO SHOW BOOKS PUBLISHED BETWEEN YEAR 2011 TO 2020')
            print('ENTER "4" TO SHOW BOOKS PUBLISHED AFTER YEAR 2020')
            try:
                year_choice = int(input("ENTER YOUR CHOICE (1-4): "))
            except ValueError:
                print("ENTER A VALID NUMBER !!")
                continue

            if year_choice == 1:
                cursor.execute(
                    "SELECT * FROM book WHERE publication_year < %s ORDER BY publication_year",
                    (2000,),
                )
            elif year_choice == 2:
                cursor.execute(
                    """
                    SELECT * FROM book
                    WHERE publication_year BETWEEN %s AND %s
                    ORDER BY publication_year
                    """,
                    (2000, 2010),
                )
            elif year_choice == 3:
                cursor.execute(
                    """
                    SELECT * FROM book
                    WHERE publication_year BETWEEN %s AND %s
                    ORDER BY publication_year
                    """,
                    (2011, 2020),
                )
            elif year_choice == 4:
                cursor.execute(
                    "SELECT * FROM book WHERE publication_year > %s ORDER BY publication_year",
                    (2020,),
                )
            else:
                print("ENTER CORRECT CHOICE !!")
                continue
        elif choice == 5:
            isbn = input("ENTER ISBN OF BOOK YOU WANT TO SEARCH: ")
            cursor.execute("SELECT * FROM book WHERE isbn = %s", (isbn,))
        elif choice == 6:
            title = input("ENTER TITLE OF BOOK YOU WANT TO SEARCH: ")
            cursor.execute("SELECT * FROM book WHERE book_title = %s", (title,))
        elif choice == 7:
            author = input("ENTER AUTHOR OF BOOK YOU WANT TO SEARCH: ")
            cursor.execute("SELECT * FROM book WHERE author_name = %s", (author,))
        elif choice == 8:
            publisher = input("ENTER PUBLISHER OF BOOK YOU WANT TO SEARCH: ")
            cursor.execute("SELECT * FROM book WHERE publisher = %s", (publisher,))
        elif choice == 9:
            try:
                year = int(input("ENTER PUBLICATION YEAR OF BOOK YOU WANT TO SEARCH: "))
            except ValueError:
                print("ENTER A VALID YEAR !!")
                continue
            cursor.execute("SELECT * FROM book WHERE publication_year = %s", (year,))
        elif choice == 10:
            book_type = input("ENTER TYPE OF BOOK YOU WANT TO SEARCH: ")
            cursor.execute("SELECT * FROM book WHERE book_type = %s", (book_type,))
        elif choice == 11:
            language = input("ENTER LANGUAGE OF BOOK YOU WANT TO SEARCH: ")
            cursor.execute("SELECT * FROM book WHERE language = %s", (language,))
        else:
            print("ENTER CORRECT CHOICE !!")
            continue

        pause()
        print("The books you searched for are:")
        print_rows(cursor.fetchall())


def add_book(connection, cursor):
    while True:
        isbn = input("ENTER ISBN OF THE BOOK: ")
        title = input("ENTER TITLE OF THE BOOK: ")
        author = input("ENTER AUTHOR OF THE BOOK: ")
        publisher = input("ENTER PUBLISHER OF THE BOOK: ")

        try:
            publication_year = int(input("ENTER PUBLICATION YEAR OF THE BOOK: "))
        except ValueError:
            print("PUBLICATION YEAR MUST BE A NUMBER.")
            continue

        book_type = input("ENTER TYPE OF THE BOOK: ")
        language = input("ENTER LANGUAGE OF THE BOOK: ")

        cursor.execute(
            """
            INSERT INTO book (
                isbn, book_title, author_name, publisher,
                publication_year, book_type, language
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (isbn, title, author, publisher, publication_year, book_type, language),
        )
        connection.commit()
        pause()
        print("BOOK SUCCESSFULLY ADDED !!")

        if input('DO YOU WANT TO ADD MORE BOOKS? (yes/no): ').strip().lower() != "yes":
            return


def update_book(connection, cursor):
    while True:
        isbn = input("ENTER ISBN OF THE BOOK YOU WANT TO UPDATE: ")
        if not fetch_book_by_isbn(cursor, isbn):
            print("BOOK NOT FOUND !!")
            continue

        print('ENTER "1" TO UPDATE BOOK TITLE')
        print('ENTER "2" TO UPDATE AUTHOR NAME')
        print('ENTER "3" TO UPDATE PUBLISHER')
        print('ENTER "4" TO UPDATE PUBLICATION YEAR')
        print('ENTER "5" TO UPDATE BOOK TYPE')
        print('ENTER "6" TO UPDATE LANGUAGE')

        try:
            choice = int(input("ENTER YOUR CHOICE (1-6): "))
        except ValueError:
            print("ENTER A VALID NUMBER !!")
            continue

        if choice == 1:
            value = input("ENTER UPDATED BOOK TITLE: ")
            query = "UPDATE book SET book_title = %s WHERE isbn = %s"
        elif choice == 2:
            value = input("ENTER UPDATED AUTHOR NAME: ")
            query = "UPDATE book SET author_name = %s WHERE isbn = %s"
        elif choice == 3:
            value = input("ENTER UPDATED PUBLISHER: ")
            query = "UPDATE book SET publisher = %s WHERE isbn = %s"
        elif choice == 4:
            try:
                value = int(input("ENTER UPDATED PUBLICATION YEAR: "))
            except ValueError:
                print("ENTER A VALID YEAR !!")
                continue
            query = "UPDATE book SET publication_year = %s WHERE isbn = %s"
        elif choice == 5:
            value = input("ENTER UPDATED BOOK TYPE: ")
            query = "UPDATE book SET book_type = %s WHERE isbn = %s"
        elif choice == 6:
            value = input("ENTER UPDATED LANGUAGE: ")
            query = "UPDATE book SET language = %s WHERE isbn = %s"
        else:
            print("ENTER CORRECT CHOICE !!")
            continue

        cursor.execute(query, (value, isbn))
        connection.commit()
        pause()
        print("SUCCESSFULLY UPDATED !!")

        if input("DO YOU WANT TO UPDATE ANYTHING ELSE? (yes/no): ").strip().lower() != "yes":
            return


def delete_book(connection, cursor):
    isbn = input("ENTER ISBN OF THE BOOK YOU WANT TO DELETE: ")
    pause()
    print("THE ITEM DELETED CANNOT BE RETRIEVED !!")
    if input("ARE YOU SURE YOU WANT TO DELETE? (y/n): ").strip().lower() == "y":
        cursor.execute("DELETE FROM book WHERE isbn = %s", (isbn,))
        connection.commit()
        pause()
        print("BOOK DELETED SUCCESSFULLY !!")
    else:
        print("NO ITEM DELETED !!")


def issue_book(connection, cursor):
    pause()
    print("ENTER THE FOLLOWING DETAILS TO ISSUE A BOOK:")
    isbn = input("ENTER ISBN OF THE BOOK YOU WANT TO ISSUE: ")

    book = fetch_book_by_isbn(cursor, isbn)
    if not book:
        print("BOOK NOT FOUND IN LIBRARY !!")
        return

    issuer_name = input("ENTER NAME OF ISSUER: ")
    date_of_issue = input("ENTER DATE OF ISSUE (YYYY-MM-DD): ")

    try:
        contact_no = int(input("ENTER CONTACT NUMBER OF THE ISSUER: "))
    except ValueError:
        print("CONTACT NUMBER MUST BE NUMERIC.")
        return

    cursor.execute(
        """
        INSERT INTO issue (isbn, book_title, issuer_name, date_of_issue, contact_no)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (isbn, book[1], issuer_name, date_of_issue, contact_no),
    )
    connection.commit()
    pause()
    print("YOU HAVE SUCCESSFULLY ISSUED THE BOOK !!")
    print("ENJOY READING !!")


def search_issued_books(cursor):
    while True:
        print('ENTER "1" TO SORT BY ISBN')
        print('ENTER "2" TO SORT BY NAME OF ISSUER')
        print('ENTER "3" TO SEARCH BY NAME OF ISSUER')
        print('ENTER "0" TO GO BACK')

        try:
            choice = int(input("ENTER YOUR CHOICE (0-3): "))
        except ValueError:
            print("ENTER A VALID NUMBER !!")
            continue

        if choice == 0:
            return
        if choice == 1:
            cursor.execute("SELECT * FROM issue ORDER BY isbn")
        elif choice == 2:
            cursor.execute("SELECT * FROM issue ORDER BY issuer_name")
        elif choice == 3:
            issuer_name = input("ENTER NAME OF ISSUER YOU WANT TO SEARCH: ")
            cursor.execute("SELECT * FROM issue WHERE issuer_name = %s", (issuer_name,))
        else:
            print("ENTER CORRECT OPTION !!")
            continue

        pause()
        print_rows(cursor.fetchall())


def update_issue_info(connection, cursor):
    while True:
        isbn = input("ENTER ISBN OF THE ISSUED BOOK YOU WANT TO EDIT: ")

        cursor.execute("SELECT * FROM issue WHERE isbn = %s", (isbn,))
        if not cursor.fetchone():
            print("ISSUE RECORD NOT FOUND !!")
            continue

        print('ENTER "1" TO UPDATE ISSUER NAME')
        print('ENTER "2" TO UPDATE DATE OF ISSUE')
        print('ENTER "3" TO UPDATE CONTACT INFO')

        try:
            choice = int(input("ENTER YOUR CHOICE (1-3): "))
        except ValueError:
            print("ENTER A VALID NUMBER !!")
            continue

        if choice == 1:
            value = input("ENTER UPDATED ISSUER NAME: ")
            query = "UPDATE issue SET issuer_name = %s WHERE isbn = %s"
        elif choice == 2:
            value = input("ENTER UPDATED DATE OF ISSUE: ")
            query = "UPDATE issue SET date_of_issue = %s WHERE isbn = %s"
        elif choice == 3:
            try:
                value = int(input("ENTER UPDATED CONTACT NUMBER: "))
            except ValueError:
                print("CONTACT NUMBER MUST BE NUMERIC.")
                continue
            query = "UPDATE issue SET contact_no = %s WHERE isbn = %s"
        else:
            print("ENTER CORRECT CHOICE !!")
            continue

        cursor.execute(query, (value, isbn))
        connection.commit()
        pause()
        print("SUCCESSFULLY UPDATED !!")

        if input("DO YOU WANT TO UPDATE MORE? (yes/no): ").strip().lower() != "yes":
            return


def delete_issuer(connection, cursor):
    isbn = input("ENTER ISBN OF THE ISSUED BOOK YOU WANT TO DELETE: ")
    pause()
    print("THE ITEM DELETED CANNOT BE RETRIEVED !!")
    if input("ARE YOU SURE YOU WANT TO DELETE? (y/n): ").strip().lower() == "y":
        cursor.execute("DELETE FROM issue WHERE isbn = %s", (isbn,))
        connection.commit()
        pause()
        print("ISSUED BOOK RECORD DELETED SUCCESSFULLY !!")
    else:
        print("NO ITEM DELETED !!")


def return_book(connection, cursor):
    pause()
    print("ENTER THE FOLLOWING DETAILS TO RETURN A BOOK:")
    isbn = input("ENTER ISBN OF THE BOOK YOU WANT TO RETURN: ")

    cursor.execute("SELECT * FROM issue WHERE isbn = %s", (isbn,))
    issued_book = cursor.fetchone()
    if not issued_book:
        print("ISSUE RECORD NOT FOUND !!")
        return

    issuer_name = input("ENTER NAME OF ISSUER: ")
    date_of_issue = input("ENTER DATE OF ISSUE (YYYY-MM-DD): ")
    date_of_return = input("ENTER DATE OF RETURN (YYYY-MM-DD): ")

    try:
        fine = float(input("ENTER FINE: "))
        contact_no = int(input("ENTER CONTACT NUMBER OF THE ISSUER: "))
    except ValueError:
        print("FINE AND CONTACT NUMBER MUST BE NUMERIC.")
        return

    cursor.execute(
        """
        INSERT INTO returns (
            isbn, book_title, issuer_name, date_of_issue,
            date_of_return, fine, contact_no
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            isbn,
            issued_book[1],
            issuer_name,
            date_of_issue,
            date_of_return,
            fine,
            contact_no,
        ),
    )
    connection.commit()
    pause()
    print("YOU HAVE SUCCESSFULLY RETURNED THE BOOK !!")


def search_returned_books(cursor):
    while True:
        print('ENTER "1" TO SORT BY ISBN')
        print('ENTER "2" TO SORT BY NAME OF ISSUER')
        print('ENTER "3" TO SEARCH BY NAME OF ISSUER')
        print('ENTER "0" TO GO BACK')

        try:
            choice = int(input("ENTER YOUR CHOICE (0-3): "))
        except ValueError:
            print("ENTER A VALID NUMBER !!")
            continue

        if choice == 0:
            return
        if choice == 1:
            cursor.execute("SELECT * FROM returns ORDER BY isbn")
        elif choice == 2:
            cursor.execute("SELECT * FROM returns ORDER BY issuer_name")
        elif choice == 3:
            issuer_name = input("ENTER NAME OF ISSUER YOU WANT TO SEARCH: ")
            cursor.execute("SELECT * FROM returns WHERE issuer_name = %s", (issuer_name,))
        else:
            print("ENTER CORRECT OPTION !!")
            continue

        pause()
        print_rows(cursor.fetchall())


def update_return_info(connection, cursor):
    while True:
        isbn = input("ENTER ISBN OF THE RETURNED BOOK YOU WANT TO EDIT: ")

        cursor.execute("SELECT * FROM returns WHERE isbn = %s", (isbn,))
        if not cursor.fetchone():
            print("RETURN RECORD NOT FOUND !!")
            continue

        print('ENTER "1" TO UPDATE ISSUER NAME')
        print('ENTER "2" TO UPDATE DATE OF RETURN')
        print('ENTER "3" TO UPDATE FINE')
        print('ENTER "4" TO UPDATE CONTACT INFO')

        try:
            choice = int(input("ENTER YOUR CHOICE (1-4): "))
        except ValueError:
            print("ENTER A VALID NUMBER !!")
            continue

        if choice == 1:
            value = input("ENTER UPDATED ISSUER NAME: ")
            query = "UPDATE returns SET issuer_name = %s WHERE isbn = %s"
        elif choice == 2:
            value = input("ENTER UPDATED DATE OF RETURN: ")
            query = "UPDATE returns SET date_of_return = %s WHERE isbn = %s"
        elif choice == 3:
            try:
                value = float(input("ENTER UPDATED FINE: "))
            except ValueError:
                print("FINE MUST BE NUMERIC.")
                continue
            query = "UPDATE returns SET fine = %s WHERE isbn = %s"
        elif choice == 4:
            try:
                value = int(input("ENTER UPDATED CONTACT NUMBER: "))
            except ValueError:
                print("CONTACT NUMBER MUST BE NUMERIC.")
                continue
            query = "UPDATE returns SET contact_no = %s WHERE isbn = %s"
        else:
            print("ENTER CORRECT CHOICE !!")
            continue

        cursor.execute(query, (value, isbn))
        connection.commit()
        pause()
        print("SUCCESSFULLY UPDATED !!")

        if input("DO YOU WANT TO UPDATE MORE? (yes/no): ").strip().lower() != "yes":
            return


def delete_return(connection, cursor):
    isbn = input("ENTER ISBN OF THE RETURNED BOOK YOU WANT TO DELETE: ")
    pause()
    print("THE ITEM DELETED CANNOT BE RETRIEVED !!")
    if input("ARE YOU SURE YOU WANT TO DELETE? (y/n): ").strip().lower() == "y":
        cursor.execute("DELETE FROM returns WHERE isbn = %s", (isbn,))
        connection.commit()
        pause()
        print("RETURN RECORD DELETED SUCCESSFULLY !!")
    else:
        print("NO ITEM DELETED !!")


def books_library(connection, cursor):
    print("***WELCOME TO BOOKS SECTION***")
    print('ENTER "1" TO SEARCH BOOKS')
    print('ENTER "2" TO ADD BOOKS')
    print('ENTER "3" TO UPDATE BOOK INFO')
    print('ENTER "4" TO DELETE A BOOK')

    try:
        choice = int(input("ENTER YOUR CHOICE: "))
    except ValueError:
        print("ENTER A VALID NUMBER !!")
        return

    if choice == 1:
        search_books(cursor)
    elif choice == 2:
        add_book(connection, cursor)
    elif choice == 3:
        update_book(connection, cursor)
    elif choice == 4:
        delete_book(connection, cursor)
    else:
        print("ENTER CORRECT OPTION !!")


def books_issue(connection, cursor):
    print("***WELCOME TO BOOK ISSUE SECTION***")
    print('ENTER "1" TO ISSUE A BOOK')
    print('ENTER "2" TO SEARCH ISSUER')
    print('ENTER "3" TO UPDATE BOOK ISSUE INFO')
    print('ENTER "4" TO DELETE AN ISSUE RECORD')

    try:
        choice = int(input("ENTER YOUR CHOICE: "))
    except ValueError:
        print("ENTER A VALID NUMBER !!")
        return

    if choice == 1:
        issue_book(connection, cursor)
    elif choice == 2:
        search_issued_books(cursor)
    elif choice == 3:
        update_issue_info(connection, cursor)
    elif choice == 4:
        delete_issuer(connection, cursor)
    else:
        print("ENTER CORRECT OPTION !!")


def books_returned(connection, cursor):
    print("***WELCOME TO BOOK RETURN SECTION***")
    print('ENTER "1" TO RETURN A BOOK')
    print('ENTER "2" TO SEARCH RETURN INFO')
    print('ENTER "3" TO UPDATE RETURN INFO')
    print('ENTER "4" TO DELETE RETURN INFO')

    try:
        choice = int(input("ENTER YOUR CHOICE: "))
    except ValueError:
        print("ENTER A VALID NUMBER !!")
        return

    if choice == 1:
        return_book(connection, cursor)
    elif choice == 2:
        search_returned_books(cursor)
    elif choice == 3:
        update_return_info(connection, cursor)
    elif choice == 4:
        delete_return(connection, cursor)
    else:
        print("ENTER CORRECT OPTION !!")


def main():
    connection = connect_server()
    cursor = connection.cursor()
    setup_database(connection, cursor)

    keep_running = "yes"
    while keep_running == "yes":
        print("WHAT WOULD YOU LIKE TO DO HERE ??")
        print('ENTER "1" TO VIEW BOOKS')
        print('ENTER "2" TO ISSUE BOOKS')
        print('ENTER "3" TO RETURN BOOKS')

        try:
            choice = int(input("ENTER YOUR CHOICE: "))
        except ValueError:
            print("ENTER A VALID NUMBER !!")
            continue

        if choice == 1:
            books_library(connection, cursor)
        elif choice == 2:
            books_issue(connection, cursor)
        elif choice == 3:
            books_returned(connection, cursor)
        else:
            print("ENTER CORRECT CHOICE !!")

        keep_running = input("DO YOU WANT TO DO SOMETHING ELSE? (yes/no): ").strip().lower()

    print("\t\t\t****THANKS FOR VISITING****")
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
