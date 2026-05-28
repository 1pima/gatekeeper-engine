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
    DECLINED = 2
    AUTHORIZED = 3
    REVERSED = 4
    CHARGED = 5
    REFUNDED = 6

    def is_possible(self, status):
        conditions = {
            self.NEW: (self.DECLINED, self.AUTHORIZED),
            self.DECLINED: (),
            self.AUTHORIZED: (self.REVERSED, self.CHARGED),
            self.REVERSED: (),
            self.CHARGED: (),
            self.REFUNDED: ()
        }
        return status in conditions[self]
