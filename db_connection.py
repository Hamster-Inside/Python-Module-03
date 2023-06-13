import sqlite3
from my_logger import MyLogger
from datetime import datetime


class DatabaseConnection:

    def __init__(self, db_path: str, log_name: str, log_file: str):
        self.logger = MyLogger(log_name, log_file).get_logger()
        self.db_path = db_path
        self.conn = self.__create_connection()
        self.cursor = self.__create_cursor()

    def __create_connection(self):
        conn = sqlite3.connect(self.db_path)
        return conn

    def __create_cursor(self):
        cursor = self.conn.cursor()
        return cursor

    def get_part_quantity(self, part_number):
        self.cursor.execute('SELECT part_quantity FROM parts WHERE part_number=?', (part_number,))
        quantity = int(self.cursor.fetchall()[0][0])
        return quantity

    def get_part_finished_status(self, part_number):
        self.cursor.execute('SELECT finished FROM parts WHERE part_number=?', (part_number,))
        finished_status = bool(self.cursor.fetchall()[0][0])
        return finished_status

    def set_part_finished(self, part_number, finished_status):
        if not self.is_present_in_db(part_number):
            return
        self.cursor.execute('UPDATE parts SET finished=? WHERE part_number=?', (finished_status, part_number))
        self.conn.commit()

    def set_parts_done_quantity(self, part_number, quantity_of_done_parts):
        if not self.is_present_in_db(part_number):
            return
        self.cursor.execute('UPDATE parts SET parts_done_quantity=? WHERE part_number=?',
                            (quantity_of_done_parts, part_number))
        self.conn.commit()

    def get_parts_done_quantity(self, part_number):
        if not self.is_present_in_db(part_number):
            return
        self.cursor.execute('SELECT parts_done_quantity FROM parts WHERE part_number=?', (part_number,))
        parts_done_quantity = int(self.cursor.fetchall()[0][0])
        return parts_done_quantity

    def set_mail_sent_status_to_part(self, part_number, mail_sent_status):
        if not self.is_present_in_db(part_number):
            return
        self.cursor.execute('UPDATE parts SET email_sent_status=? WHERE part_number=?', (mail_sent_status, part_number))
        self.conn.commit()

    def set_new_quantity_to_part(self, part_number, new_quantity):
        if not self.is_present_in_db(part_number):
            return
        self.cursor.execute('UPDATE parts SET part_quantity=? WHERE part_number=?', (new_quantity, part_number))
        self.conn.commit()

    def is_present_in_db(self, part_number):
        self.cursor.execute('SELECT * FROM parts WHERE part_number=?', (part_number,))
        result = self.cursor.fetchone()
        if result is not None:
            return True
        else:
            self.logger.info(f'Part number: {part_number} is not in db')
            return False

    def add_part_to_db(self, part_number, quantity, deadline='2500-01-01 00:00:00'):
        if self.is_present_in_db(part_number):
            self.logger.info(f'Part number: {part_number} already exists in database')
            return
        print('added')
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # %f for microseconds, %S for seconds
        self.cursor.execute('INSERT INTO parts (part_number, part_quantity, finished, created_at, deadline_date) '
                            'VALUES (?, ?, FALSE, ?, ?)',
                            (part_number, quantity, current_date, deadline))
        self.conn.commit()

    def get_all_parts(self):
        self.cursor.execute('SELECT part_number FROM parts')
        response = self.cursor.fetchall()
        list_of_all_parts = []
        for row in response:
            if list_of_all_parts.__contains__(row[0]):
                self.logger.warn(f'Multiple part in database: {row[0]}')
                continue
            list_of_all_parts.append(row[0])
        return list_of_all_parts
