import logging

logger = logging.getLogger(__name__)


class YtDlpLogger:
    def __init__(self, trigger_string: str | None = None, callback=None):
        self.trigger_string = trigger_string
        self.callback = callback

    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            logger.debug(msg)
            self.check_trigger(msg)
        else:
            self.info(msg)

    def info(self, msg):
        logger.info(msg)
        self.check_trigger(msg)

    def warning(self, msg):
        logger.warn(msg)
        self.check_trigger(msg)

    def error(self, msg):
        logger.error(msg)
        self.check_trigger(msg)

    def check_trigger(self, message):
        if self.trigger_string and self.trigger_string in message:
            self.callback(message)
