# logging_utils.py
import logging

def setup_logger(name="canvasutils", level=logging.INFO, logfile=None, console=False):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # avoid adding handlers twice
    if not logger.handlers:
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # console
        if console:
            ch = logging.StreamHandler()
            ch.setFormatter(fmt)
            logger.addHandler(ch)

        # optional file logging
        if logfile:
            fh = logging.FileHandler(logfile)
            fh.setFormatter(fmt)
            logger.addHandler(fh)

    return logger