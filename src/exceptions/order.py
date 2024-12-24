from src.exceptions.base import CloudSellAPIException


class OrderInsertFailed(CloudSellAPIException):
    ...

class OrderDeleteFailed(CloudSellAPIException):
    ...

class OrderNotFound(CloudSellAPIException):
    ...

class OrderAlreadyExists(CloudSellAPIException):
    ...

class FailedToCreateOrder(CloudSellAPIException):
    ...

class NoAccessOrder(CloudSellAPIException):
    ...