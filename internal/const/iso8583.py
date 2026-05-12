from enum import Enum


class TransactionType(Enum):
    ServicePurchase = '00'
    """Электронная коммерция"""
    ATMWithdrawal = '01'
    """Снятие через АТМ"""
    AccountFunding = '10'
    """Списание при p2p"""
    CashAdvance = '17'
    """Оплата с POS-терминала"""
    Payment = '28'
    """Пополние при p2p переводе/пополнение баланса карты"""
    CashIn = '29'
    """Внесение наличных через АТМ"""
    BalanceInquiry = '30'
    """Запрос баланса карты"""
    MiniStatement = '32'
    """Минивыписка о последних 10 операциях по карте"""

    Unique = '11'  # Unique transactions from WAY4 might have processing code ‘00’ as well as ‘11’ for transit from VISA/MC
    PurchaseReturn = '20'  # Value 20 is allowed for VISA and MasterCard transactions
    AccountVerification = '39'
    CardControl = '91'
    PinChange = '92'
