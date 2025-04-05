# sliver-notify
client to send notifications of new/removed beacons, as well as some basic commands for interacting with sessions. plans to add more commands, improve display of dead beacons and generally improve the structure and code

1. create `config.py`

2. add your token, chat_id(@userinfobot) and sliver config file to it

```
import logging
from colorlog import ColoredFormatter
import re

# @userinfobot
CHAT_ID = "YOUR_CHAT_ID"
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
#CONFIG_PATH = os.path.join('', 'to', 'default.cfg')
CFG_PATH = "YOUR_SLIVER_CONFIG_FILE_PATH"

UUID_REGEX = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

log_format = (
    "%(log_color)s[%(asctime)s] [%(levelname)s]%(reset)s %(message_log_color)s%(message)s"
)
date_format = "%H:%M:%S"
formatter = ColoredFormatter(
    log_format,
    datefmt=date_format,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    secondary_log_colors={
        "message": {
            "DEBUG": "cyan",
            "INFO": "white",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        }
    },
    style="%",
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers = [handler]
```

4. or test it online, u can create some test config in sliver and import it into @sliver_notify_bot (not always available)

i'll add more convenient config file later, this is just a test case
