import logging
import sys

log_format = "[%(levelname)s] - %(module)s.function.%(funcName)s --> %(message)s"

logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(log_format))

logger.addHandler(console_handler)
