# COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)

RED = (255,0,0)
GREEN1= (0,255,0)
GREEN2 = (0,102,0)
GREEN3 = (0,55,0)
BLUE = (0,0,255)

YELLOW = (255,255,0)


# PATHS
from pathlib import Path
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RUN_DIR = DATA_DIR / timestamp

DATA_DIR.mkdir(parents=True, exist_ok=True)
RUN_DIR.mkdir(parents=True, exist_ok=True)


# LOGGER
import logging

LOG_FILENAME = "app.log"

# CONFIGURACIÓN DEL LOGGER 
logger = logging.getLogger("app_logger")  
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if logger.hasHandlers():
    logger.handlers.clear()

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Handler para archivo
file_handler = logging.FileHandler(RUN_DIR / LOG_FILENAME) 
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
