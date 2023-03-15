import logging


class MyLogger:

    def __init__(self, log_name, log_file_name):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)

        # create file handler and set level to debug
        fh = logging.FileHandler(log_file_name)
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
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger
