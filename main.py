from db_connection import DatabaseConnection
from email_sender import EmailSender
from os import getenv
from dotenv import load_dotenv
from collections import namedtuple

if __name__ == '__main__':
    load_dotenv()
    db = DatabaseConnection(getenv('DB_FILE'), 'PARTS DB', 'my_log_file.log')

    Credentials = namedtuple('Credentials', 'username, password')
    credentials = Credentials(getenv('EMAIL'), getenv('GMAIL_PASSWORD_FOR_APPLICATION'))
    ssl_enabled = getenv('SSL_ENABLED')
    port = getenv('PORT')
    smtp_server = getenv('SMTP_SERVER')

    # sending email with own context manager
    with EmailSender(port, smtp_server, credentials, ssl_enabled) as connection:
        connection.send_mail('stefan.zlotolubny@gmail.com', 'KOKOS', 'random message')

    # conn = db.create_connection()
    # if not db.is_present_in_db(conn, part_number):
    #     conn = db.create_connection()
    #     db.add_part_to_db(conn, part_number, 3, "2023.10.10 15:37:00")
    # else:
    #     db.logger.info(f'Part {part_number} already exists in database, you cannot add another one as new')
    # conn = db.create_connection() # <--- Have to create connection before every method on db
    # print(db.get_all_parts(conn))

    part_number = '999888777-666-55-1002'
    conn = db.create_connection()
    print(f'Quantity of part {part_number} -> {db.get_parts_done_quantity(conn, "999888777-666-55-1002")}')
