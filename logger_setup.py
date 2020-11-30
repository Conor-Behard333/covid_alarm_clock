"""Sets up a logger than can be used for different modules"""
import logging


def setup_logger(logger_name, test):
    """creates a logger and changes its settings:

    :return: logger object
    """

    # Creates a logger called "log" and sets its logging level to DEBUG
    logger = logging.getLogger(test)
    logger.setLevel(logging.DEBUG)

    # Creates a log file to write messages to
    handler = logging.FileHandler(f'log files/{logger_name}', 'w', 'utf-8')

    # Formats messages in the log with the name of the logger and then the message
    handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger
