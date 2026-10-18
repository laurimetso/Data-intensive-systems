# Database Manager (Assignment 2)

## Description

A simple Python program that manages three separate SQLite databases: Students, Courses, and Library.

Users can select a database through a menu and view, add, edit, and delete records.

## Features

- Three separate SQLite databases
- Automatically creates database files and tables
- Includes dummy data for testing
- View existing records
- Add new records
- Edit existing records
- Delete records
- Simple command-line interface

## Technologies

- Python 3
- SQLite (`sqlite3` standard library)

## How to Run

1. Install Python 3 if it is not already installed.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python demo.py
   ```

The database files and sample data are created automatically when the program starts.

## Databases

| Database | Contents |
|---|---|
| Students | Student names, emails, majors, and study years |
| Courses | Course codes, titles, credits, and teachers |
| Library | Book titles, authors, genres, and copy counts |

## Assignment

This project was created for Assignment 2 and demonstrates database access and data modification using three separate SQLite databases.
