from db_connection import DatabaseConnection

db = DatabaseConnection('mod3_database_01.db')
db.set_loggers('PARTS DB', 'my_log_file.log')



part_number = "123456789-1111-1007"

conn = db.create_connection()
if not db.is_present_in_db(conn, part_number):
    conn = db.create_connection()
    db.add_part_to_db(conn, part_number, 3, "2023.10.10 15:37:00")

else:
    db.logger.info(f'Part {part_number} already exists in database, you cannot add another one as new')
