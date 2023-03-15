import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger('DB_Log')
logger.setLevel(logging.DEBUG)

# create file handler and set level to debug
fh = logging.FileHandler('my_log_file.log')
fh.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to handlers
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add handlers to logger
logger.addHandler(fh)
logger.addHandler(ch)


class DatabaseConnection:

    def __init__(self, db_path):
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

    def set_part_finished(self, part_name):
        pass

    def set_new_quantity_to_part(self, part_number, new_quantity):
        self.cursor.execute('UPDATE parts SET part_quantity=? WHERE part_number=?', (new_quantity, part_number))
        self.conn.commit()

    def check_if_part_exists(self, part_number):
        self.cursor.execute('SELECT * FROM parts WHERE part_number=?', (part_number,))
        result = self.cursor.fetchone()
        if result is not None:
            return True
        else:
            return False

    def add_part_to_db(self, part_number, quantity, deadline='2500-01-01 00:00:00'):
        if self.check_if_part_exists(part_number):
            logger.info(f'Part number: {part_number} already exists in database')
            return
        print('added')
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # %f for microseconds, %S for seconds
        self.cursor.execute('INSERT INTO parts (part_number, part_quantity, finished, created_at, deadline_date) '
                            'VALUES (?, ?, FALSE, ?, ?)',
                            (part_number, quantity, current_date, deadline))
        self.conn.commit()


db = DatabaseConnection('mod3_database_01.db')
print(db.get_part_quantity('999888777-666-55-1007'))
print(db.check_if_part_exists('999888777-666-55-1007'))
db.add_part_to_db('999666111-000-00-0001', 777)
print(db.get_part_finished_status('999888777-666-55-1005'))
