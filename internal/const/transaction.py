from enum import IntEnum


class Currency(IntEnum):
    KZT = 398
    RUB = 643
    USD = 840
    EUR = 978
    UZS = 860
    KGS = 417
    TJS = 972


class TransactionStatus(IntEnum):
    NEW = 1
    AUTHORIZED = 2
    REVERSED = 3
    CHARGED = 4
    REFUNDED = 5
