import sqlite3
from my_logger import MyLogger
from datetime import datetime
from database import Database


class DatabaseConnection:

    def __init__(self, db_path: str ,log_name='', log_file=''):
        self.db_path = db_path
        self.set_loggers(log_name, log_file)

    def set_loggers(self, log_name: str, log_file: str):
        if log_name == '':
            log_name = 'TEMP_LOG'
        if log_file == '':
            log_file = 'TEMP_LOG.log'
        self.logger = MyLogger(log_name, log_file).get_logger()

    def create_connection(self):
        return sqlite3.connect(self.db_path)

    def create_new_parts_database_file(self, db_file_name):
        try:
            conn = sqlite3.connect(db_file_name)
            cursor = conn.cursor()
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
            conn.commit()
            self.db_path = db_file_name
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def get_part_quantity(self, connection, part_number):
        with Database(connection) as db:
            db.cursor.execute('SELECT part_quantity FROM parts WHERE part_number=?', (part_number,))
            quantity = int(db.cursor.fetchall()[0][0])
            return quantity

    def get_part_finished_status(self, connection, part_number):
        with Database(connection) as db:
            db.cursor.execute('SELECT finished FROM parts WHERE part_number=?', (part_number,))
            finished_status = bool(db.cursor.fetchall()[0][0])
            return finished_status

    def set_part_finished(self, connection, part_number, finished_status):
        with Database(connection) as db:
            db.cursor.execute('UPDATE parts SET finished=? WHERE part_number=?', (finished_status, part_number))

    def set_parts_done_quantity(self, connection, part_number, quantity_of_done_parts):
        with Database(connection) as db:
            db.cursor.execute('UPDATE parts SET parts_done_quantity=? WHERE part_number=?',
                              (quantity_of_done_parts, part_number))

    def get_parts_done_quantity(self, connection, part_number):
        with Database(connection) as db:
            db.cursor.execute('SELECT parts_done_quantity FROM parts WHERE part_number=?', (part_number,))
            parts_done_quantity = int(db.cursor.fetchall()[0][0])
            return parts_done_quantity

    def set_mail_sent_status_to_part(self, connection, part_number, mail_sent_status):
        with Database(connection) as db:
            db.cursor.execute('UPDATE parts SET email_sent_status=? WHERE part_number=?',
                              (mail_sent_status, part_number))

    def set_new_quantity_to_part(self, connection, part_number, new_quantity):
        with Database(connection) as db:
            db.cursor.execute('UPDATE parts SET part_quantity=? WHERE part_number=?', (new_quantity, part_number))

    def is_present_in_db(self, connection, part_number):
        with Database(connection) as db:
            db.cursor.execute('SELECT * FROM parts WHERE part_number=?', (part_number,))
            result = db.cursor.fetchone()
        if result is not None:
            return True
        else:
            return False

    def add_part_to_db(self, connection, part_number, quantity, deadline='2500-01-01 00:00:00'):
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # %f for microseconds, %S for seconds
        with Database(connection) as db:
            db.cursor.execute('INSERT INTO parts (part_number, part_quantity, finished, created_at, deadline_date) '
                              'VALUES (?, ?, FALSE, ?, ?)',
                              (part_number, quantity, current_date, deadline))
            print("added part: " + part_number)

    def get_all_parts(self, connection):
        with Database(connection) as db:
            db.cursor.execute('SELECT part_number FROM parts')
            response = db.cursor.fetchall()
        list_of_all_parts = []
        for row in response:
            if list_of_all_parts.__contains__(row[0]):
                self.logger.warn(f'Multiple part in database: {row[0]}')
                continue
            list_of_all_parts.append(row[0])
        return list_of_all_parts
