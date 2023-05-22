from flask import request

from app.log import CorrelationLoggerDecorator
from app.user.model import User


class BaseService:
    def __init__(self, service_name, user: User = None, parent_logger=None) -> None:
        if parent_logger is None:
            self.logger: CorrelationLoggerDecorator = request.logger.getChild(service_name)
        else:
            self.logger: CorrelationLoggerDecorator = parent_logger.getChild(service_name)
        if user is not None:
            self.logger.base = {**self.logger.base, "user": user.id}
            self.user = user
        else:
            self.user = None