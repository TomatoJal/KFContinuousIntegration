import logging
import logging.handlers


class LogConstant:
    """日志模块常量"""
    LOG_REPORT_FORMAT = '%(asctime)s [%(filename)-10s lineno:%(lineno)-4d] %(levelname)-7s : %(message)s'
    # LOG_REPORT_FORMAT = '%(asctime)s : %(message)s'
    LOG_REPORT_PLACEHOLDER = 26


def create_stream_handler(level):
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(LogConstant.LOG_REPORT_FORMAT)
    handler.setFormatter(formatter)
    return handler


class Log(object):

    def __init__(self):
        self.level = logging.DEBUG
        self._reportLogger = None

    @property
    def log(self):
        if self._reportLogger:
            return self._reportLogger
        self._reportLogger = logging.getLogger("kfLog")
        self._reportLogger.addHandler(create_stream_handler(self.level))
        self._reportLogger.setLevel(self.level)
        return self._reportLogger



log = Log()
debug = log.log.debug
info = log.log.info
warn = log.log.warning
error = log.log.error


if __name__ == '__main__':
    info('info')
    warn('warn')
    error('error')



