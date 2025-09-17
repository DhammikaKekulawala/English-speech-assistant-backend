import logging
import sys


def get_logger(name: str = __name__) -> logging.Logger:
	logger = logging.getLogger(name)
	if not logger.handlers:
		handler = logging.StreamHandler(sys.stdout)
		formatter = logging.Formatter(
			'%(asctime)s | %(levelname)-7s | %(name)s | %(message)s'
		)
		handler.setFormatter(formatter)
		logger.addHandler(handler)
	logger.setLevel(logging.INFO)
	return logger