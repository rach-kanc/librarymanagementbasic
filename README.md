# Library Management System

This project is a simple Library Management System built using Python and MySQL.

Original project was build in class 12th with python and mysql connectivity and later frontend was added .

The application now includes a basic web interface built with HTML, CSS, and JavaScript, while still using Python and MySQL as the backend.

## Features

- Add, update, delete, and search books
- Issue books and manage issued records
- Return books and manage return records
- View data in clean tables with a white-themed frontend
- Dashboard counters for books, issued books, and returned books

## Tech Stack

- Python
- Flask
- MySQL
- HTML
- CSS
- JavaScript

## Project Structure

```text
librarymanagementbasic/
|-- library.py
|-- seed_data.py
|-- templates/
|   `-- index.html
|-- static/
|   |-- style.css
|   `-- app.js
|-- .env
`-- README.md
```

## Setup

1. Make sure MySQL is installed and running.
2. Update the `.env` file with your MySQL credentials:

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
```

3. Install required Python packages:

```powershell
pip install flask mysql-connector-python
```

4. Run the application:

```powershell
python library.py
```

5. Open the browser and visit:

```text
http://127.0.0.1:5000/
```

## Test Data

To insert sample records into the database, run:

```powershell
python seed_data.py
```

## Notes

- The database name used by the project is `library`.
- Tables are created automatically when the app starts.
- The frontend is intentionally simple and uses basic HTML, CSS, and JavaScript.


