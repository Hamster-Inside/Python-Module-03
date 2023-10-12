import logging
import sys

class MyLogger:

    def __init__(self, log_name, log_file_name):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)

        # create file handler and set level to debug
        self.fh = logging.FileHandler(log_file_name)
        self.fh.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        self.ch = logging.StreamHandler(sys.stdout)
        self.ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(
            '%(asctime)s,%(msecs)03d - %(name)s - [%(filename)s:%(lineno)d]- %(levelname)s - %(message)s',
            '%Y-%m-%d %H:%M:%S')
        # add formatter to handlers
        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)

        # add handlers to logger
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

    def get_logger(self):
        return self.logger

    def change_logger_name(self, new_name):
        self.logger.name = new_name

