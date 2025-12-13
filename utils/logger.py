import logging

logger = logging.getLogger("TODO_APP")

handler = logging.StreamHandler()
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.setLevel(logging.INFO)