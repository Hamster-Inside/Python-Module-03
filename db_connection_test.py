import sqlite3
import pytest
from db_connection import DatabaseConnection


@pytest.fixture
def create_connection():
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE parts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_number TEXT NOT NULL,
                part_quantity INTEGER NOT NULL,
                finished BOOLEAN,
                created_at DATE,
                deadline_date DATE,
                parts_done_quantity INTEGER NOT NULL DEFAULT '0',
                email_sent_status BOOLEAN DEFAULT 'FALSE'
                )''')
    sample_data = [
        (1, '1111-111-1001', 3, False, '2020-03-03 10:00:00', '2023-02-06 15:00:00', 0, False),
        (2, '1111-111-1002', 5, False, '2020-03-03 11:00:00', '2025-02-04 16:00:00', 0, False),
        (3, '1111-111-1003', 6, False, '2020-03-03 14:00:00', '2026-02-03 17:00:00', 0, False)
    ]
    cursor.executemany('INSERT INTO parts VALUES (?, ?, ?, ?, ?, ?, ?, ?)', sample_data)

    return connection


def test_get_all_parts(create_connection):
    db = DatabaseConnection('')
    all_parts = db.get_all_parts(create_connection)
    assert all_parts == ['1111-111-1001', '1111-111-1002', '1111-111-1003']
