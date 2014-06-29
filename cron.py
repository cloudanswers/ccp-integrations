import logging
from commands import sync_pivotal_to_toggl

logging.basicConfig(level=logging.DEBUG)

sync_pivotal_to_toggl.sync()