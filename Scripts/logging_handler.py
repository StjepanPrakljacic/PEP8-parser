# custom_logging.py
import logging.config
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """
    A custom logging formatter that adds color to log messages based on log
    levels.

    Class Attributes:
        COLORS (dict): Mapping between log levels and ANSI escape codes for
        color and brightness.

    Methods:
        format(self, record):
            Override the format method to customize log record formatting.

    Usage:
        # Initialize the ColoredFormatter
        colored_formatter = ColoredFormatter()

        # Create a logger and set the formatter
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        handler.setFormatter(colored_formatter)
        logger.addHandler(handler)

        # Log messages with color-coded log levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
    """
    COLORS = {
        'DEBUG': Fore.CYAN + Style.BRIGHT,
        'INFO': Fore.GREEN + Style.BRIGHT,
        'WARNING': Fore.YELLOW + Style.BRIGHT,
        'ERROR': Fore.RED + Style.BRIGHT,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
           record.levelname = f"{self.COLORS[levelname]}{levelname}" \
                   f"{Style.RESET_ALL}"
        return super().format(record)

logging.config.fileConfig('logging_config.ini', disable_existing_loggers=False)
log_obj = logging.getLogger("projectLogger")
for handler in log_obj.handlers:
    handler.setFormatter(ColoredFormatter(
        '[%(asctime)s] - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'))
