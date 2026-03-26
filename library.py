"""Web-based library management app using Python, MySQL, and Flask."""

from __future__ import annotations

import os
from contextlib import closing

import mysql.connector as my
from flask import Flask, jsonify, render_template, request


def load_env_file(path=".env"):
    """Load simple KEY=VALUE pairs from a local .env file."""
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value


load_env_file()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
}
DB_NAME = "library"

BOOK_COLUMNS = [
    "isbn",
    "book_title",
    "author_name",
    "publisher",
    "publication_year",
    "book_type",
    "language",
]
ISSUE_COLUMNS = [
    "isbn",
    "book_title",
    "issuer_name",
    "date_of_issue",
    "contact_no",
]
RETURN_COLUMNS = [
    "isbn",
    "book_title",
    "issuer_name",
    "date_of_issue",
    "date_of_return",
    "fine",
    "contact_no",
]

app = Flask(__name__)


def connect_server():
    """Connect to the MySQL server."""
    return my.connect(**DB_CONFIG)


def get_connection():
    connection = connect_server()
    connection.database = DB_NAME
    return connection


def setup_database():
    """Create the database and required tables if they do not exist."""
    with closing(connect_server()) as connection:
        with closing(connection.cursor()) as cursor:
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

            # Keep older local databases in sync with the current schema.
            cursor.execute("ALTER TABLE book MODIFY isbn VARCHAR(20)")
            cursor.execute("ALTER TABLE issue MODIFY isbn VARCHAR(20)")
            cursor.execute("ALTER TABLE returns MODIFY isbn VARCHAR(20)")
            connection.commit()


def row_to_dict(columns, row):
    return {column: row[index] for index, column in enumerate(columns)}


def fetch_all(query, params, columns):
    with closing(get_connection()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(query, params)
            return [row_to_dict(columns, row) for row in cursor.fetchall()]


def fetch_one(query, params, columns=None):
    with closing(get_connection()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row is None:
                return None
            if columns is None:
                return row
            return row_to_dict(columns, row)


def execute_write(query, params):
    with closing(get_connection()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(query, params)
            connection.commit()


def parse_json(required_fields):
    data = request.get_json(silent=True) or {}
    missing = [field for field in required_fields if str(data.get(field, "")).strip() == ""]
    if missing:
        return None, jsonify({"error": f"Missing required field(s): {', '.join(missing)}"}), 400
    return data, None, None


def success_response(message, status=200):
    return jsonify({"message": message}), status


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/books", methods=["GET"])
def list_books():
    search = request.args.get("search", "").strip()
    query = """
        SELECT isbn, book_title, author_name, publisher,
               publication_year, book_type, language
        FROM book
    """
    params = ()
    if search:
        wildcard = f"%{search}%"
        query += """
            WHERE isbn LIKE %s OR book_title LIKE %s OR author_name LIKE %s
               OR publisher LIKE %s OR book_type LIKE %s OR language LIKE %s
               OR CAST(publication_year AS CHAR) LIKE %s
        """
        params = (wildcard, wildcard, wildcard, wildcard, wildcard, wildcard, wildcard)
    query += " ORDER BY book_title, isbn"
    return jsonify(fetch_all(query, params, BOOK_COLUMNS))


@app.route("/api/books", methods=["POST"])
def create_book():
    data, error_response, status = parse_json(
        ["isbn", "book_title", "author_name", "publisher", "publication_year", "book_type", "language"]
    )
    if error_response:
        return error_response, status

    existing = fetch_one("SELECT isbn FROM book WHERE isbn = %s", (data["isbn"],))
    if existing:
        return jsonify({"error": "A book with this ISBN already exists."}), 409

    execute_write(
        """
        INSERT INTO book (
            isbn, book_title, author_name, publisher,
            publication_year, book_type, language
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["isbn"],
            data["book_title"],
            data["author_name"],
            data["publisher"],
            int(data["publication_year"]),
            data["book_type"],
            data["language"],
        ),
    )
    return success_response("Book added successfully.", 201)


@app.route("/api/books/<isbn>", methods=["PUT"])
def update_book(isbn):
    data, error_response, status = parse_json(
        ["book_title", "author_name", "publisher", "publication_year", "book_type", "language"]
    )
    if error_response:
        return error_response, status

    existing = fetch_one("SELECT isbn FROM book WHERE isbn = %s", (isbn,))
    if not existing:
        return jsonify({"error": "Book not found."}), 404

    execute_write(
        """
        UPDATE book
        SET book_title = %s,
            author_name = %s,
            publisher = %s,
            publication_year = %s,
            book_type = %s,
            language = %s
        WHERE isbn = %s
        """,
        (
            data["book_title"],
            data["author_name"],
            data["publisher"],
            int(data["publication_year"]),
            data["book_type"],
            data["language"],
            isbn,
        ),
    )
    return success_response("Book updated successfully.")


@app.route("/api/books/<isbn>", methods=["DELETE"])
def delete_book(isbn):
    existing = fetch_one("SELECT isbn FROM book WHERE isbn = %s", (isbn,))
    if not existing:
        return jsonify({"error": "Book not found."}), 404

    execute_write("DELETE FROM book WHERE isbn = %s", (isbn,))
    return success_response("Book deleted successfully.")


@app.route("/api/issues", methods=["GET"])
def list_issues():
    search = request.args.get("search", "").strip()
    query = """
        SELECT isbn, book_title, issuer_name, date_of_issue, contact_no
        FROM issue
    """
    params = ()
    if search:
        wildcard = f"%{search}%"
        query += """
            WHERE isbn LIKE %s OR book_title LIKE %s OR issuer_name LIKE %s
               OR date_of_issue LIKE %s OR CAST(contact_no AS CHAR) LIKE %s
        """
        params = (wildcard, wildcard, wildcard, wildcard, wildcard)
    query += " ORDER BY date_of_issue DESC, isbn"
    return jsonify(fetch_all(query, params, ISSUE_COLUMNS))


@app.route("/api/issues", methods=["POST"])
def create_issue():
    data, error_response, status = parse_json(["isbn", "issuer_name", "date_of_issue", "contact_no"])
    if error_response:
        return error_response, status

    book = fetch_one("SELECT * FROM book WHERE isbn = %s", (data["isbn"],), BOOK_COLUMNS)
    if not book:
        return jsonify({"error": "Book not found in library."}), 404

    existing = fetch_one("SELECT isbn FROM issue WHERE isbn = %s", (data["isbn"],))
    if existing:
        return jsonify({"error": "This book is already issued."}), 409

    execute_write(
        """
        INSERT INTO issue (isbn, book_title, issuer_name, date_of_issue, contact_no)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data["isbn"],
            book["book_title"],
            data["issuer_name"],
            data["date_of_issue"],
            int(data["contact_no"]),
        ),
    )
    return success_response("Book issued successfully.", 201)


@app.route("/api/issues/<isbn>", methods=["PUT"])
def update_issue(isbn):
    data, error_response, status = parse_json(["issuer_name", "date_of_issue", "contact_no"])
    if error_response:
        return error_response, status

    existing = fetch_one("SELECT isbn FROM issue WHERE isbn = %s", (isbn,))
    if not existing:
        return jsonify({"error": "Issue record not found."}), 404

    execute_write(
        """
        UPDATE issue
        SET issuer_name = %s,
            date_of_issue = %s,
            contact_no = %s
        WHERE isbn = %s
        """,
        (
            data["issuer_name"],
            data["date_of_issue"],
            int(data["contact_no"]),
            isbn,
        ),
    )
    return success_response("Issue record updated successfully.")


@app.route("/api/issues/<isbn>", methods=["DELETE"])
def delete_issue(isbn):
    existing = fetch_one("SELECT isbn FROM issue WHERE isbn = %s", (isbn,))
    if not existing:
        return jsonify({"error": "Issue record not found."}), 404

    execute_write("DELETE FROM issue WHERE isbn = %s", (isbn,))
    return success_response("Issue record deleted successfully.")


@app.route("/api/returns", methods=["GET"])
def list_returns():
    search = request.args.get("search", "").strip()
    query = """
        SELECT isbn, book_title, issuer_name, date_of_issue,
               date_of_return, fine, contact_no
        FROM returns
    """
    params = ()
    if search:
        wildcard = f"%{search}%"
        query += """
            WHERE isbn LIKE %s OR book_title LIKE %s OR issuer_name LIKE %s
               OR date_of_issue LIKE %s OR date_of_return LIKE %s
               OR CAST(fine AS CHAR) LIKE %s OR CAST(contact_no AS CHAR) LIKE %s
        """
        params = (wildcard, wildcard, wildcard, wildcard, wildcard, wildcard, wildcard)
    query += " ORDER BY date_of_return DESC, isbn"
    return jsonify(fetch_all(query, params, RETURN_COLUMNS))


@app.route("/api/returns", methods=["POST"])
def create_return():
    data, error_response, status = parse_json(
        ["isbn", "issuer_name", "date_of_issue", "date_of_return", "fine", "contact_no"]
    )
    if error_response:
        return error_response, status

    issued_book = fetch_one("SELECT * FROM issue WHERE isbn = %s", (data["isbn"],), ISSUE_COLUMNS)
    if not issued_book:
        return jsonify({"error": "Issue record not found for this ISBN."}), 404

    existing = fetch_one("SELECT isbn FROM returns WHERE isbn = %s", (data["isbn"],))
    if existing:
        return jsonify({"error": "This return record already exists."}), 409

    execute_write(
        """
        INSERT INTO returns (
            isbn, book_title, issuer_name, date_of_issue,
            date_of_return, fine, contact_no
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["isbn"],
            issued_book["book_title"],
            data["issuer_name"],
            data["date_of_issue"],
            data["date_of_return"],
            float(data["fine"]),
            int(data["contact_no"]),
        ),
    )
    return success_response("Book return recorded successfully.", 201)


@app.route("/api/returns/<isbn>", methods=["PUT"])
def update_return(isbn):
    data, error_response, status = parse_json(
        ["issuer_name", "date_of_issue", "date_of_return", "fine", "contact_no"]
    )
    if error_response:
        return error_response, status

    existing = fetch_one("SELECT isbn FROM returns WHERE isbn = %s", (isbn,))
    if not existing:
        return jsonify({"error": "Return record not found."}), 404

    execute_write(
        """
        UPDATE returns
        SET issuer_name = %s,
            date_of_issue = %s,
            date_of_return = %s,
            fine = %s,
            contact_no = %s
        WHERE isbn = %s
        """,
        (
            data["issuer_name"],
            data["date_of_issue"],
            data["date_of_return"],
            float(data["fine"]),
            int(data["contact_no"]),
            isbn,
        ),
    )
    return success_response("Return record updated successfully.")


@app.route("/api/returns/<isbn>", methods=["DELETE"])
def delete_return(isbn):
    existing = fetch_one("SELECT isbn FROM returns WHERE isbn = %s", (isbn,))
    if not existing:
        return jsonify({"error": "Return record not found."}), 404

    execute_write("DELETE FROM returns WHERE isbn = %s", (isbn,))
    return success_response("Return record deleted successfully.")


@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    with closing(get_connection()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT COUNT(*) FROM book")
            total_books = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM issue")
            total_issues = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM returns")
            total_returns = cursor.fetchone()[0]

    return jsonify(
        {
            "total_books": total_books,
            "total_issues": total_issues,
            "total_returns": total_returns,
        }
    )


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
