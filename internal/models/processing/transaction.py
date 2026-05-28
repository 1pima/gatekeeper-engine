from datetime import datetime
import uuid
from decimal import Decimal

from blinker import Signal
from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime, Numeric, Integer, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from internal.const import exc
from internal.models.base import BaseModel
from internal.const.iso8583 import TransactionType
from internal.const.transaction import Currency, TransactionStatus


class Transaction(BaseModel):
    """
    Данные о транзакции iso8583
    """
    __tablename__ = 'transaction'
    __table_args__ = {'schema': 'processing'}

    after_created = Signal('sends after transaction created')
    after_authorized = Signal('sends after transaction authorized')

    id = Column(Uuid, primary_key=True, default=uuid.uuid7) # noqa

    reference = Column(String, nullable=False)
    ext_id = Column(String, nullable=False)
    tr_type = Column('type', ChoiceType(TransactionType, impl=String()), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    authorized_at = Column(DateTime, nullable=True)

    transaction_amount = Column(Numeric(15, 2), nullable=False)
    transaction_currency = Column(ChoiceType(Currency, impl=Integer()), nullable=False)
    settlement_amount = Column(Numeric(15, 2), nullable=False)
    settlement_currency = Column(ChoiceType(Currency, impl=Integer()), nullable=False)
    bank_data = Column(JSONB, default={})
    add_info = Column(JSONB, default={})

    token_id = Column(BigInteger, ForeignKey('vault.token.id'), nullable=False)
    token = relationship('TokenData', back_populates='transactions')

    mcc_id = Column(BigInteger, ForeignKey('catalog.mcc.id'), nullable=False)
    mcc = relationship('MCC')

    status_history = relationship('StatusHistory', back_populates='transaction', lazy='dynamic')
    status_actual = relationship(
        'StatusHistory',
        primaryjoin="and_(Transaction.id == StatusHistory.transaction_id, StatusHistory.is_actual == True)",
        uselist=False,
        viewonly=True,
        lazy='joined'
    )
    status: TransactionStatus = association_proxy('status_actual', 'status')

    def __repr__(self):
        return f'<Transaction #{self.id} [{self.reference}/{self.ext_id}]>'

    @classmethod
    def create(cls,
               reference: str,
               ext_id: str,
               tr_type: TransactionType,
               transaction_amount: Decimal,
               transaction_currency: Currency,
               settlement_amount: Decimal,
               settlement_currency: Currency,
               bank_data: dict,
               token_id: int,
               mcc_id: int,
               ):
        transaction = cls()
        transaction.reference = reference
        transaction.ext_id = ext_id
        transaction.tr_type = tr_type
        transaction.transaction_amount = transaction_amount
        transaction.transaction_currency = transaction_currency
        transaction.settlement_amount = settlement_amount
        transaction.settlement_currency = settlement_currency
        transaction.bank_data = bank_data
        transaction.token_id = token_id
        transaction.mcc_id = mcc_id
        cls.query.session.add(transaction)
        cls.query.session.commit()
        cls.after_created.send(transaction)
        return transaction

    def authorize(self, mps_code: str, mps_message: str):
        self.authorized_at = datetime.utcnow()
        self.query.session.commit()
        self._change_status(TransactionStatus.AUTHORIZED, mps_code, mps_message)

        self.after_authorized.send(self)

    def _change_status(self, status: TransactionStatus, mps_code: str, mps_message: str, desc: str = None):
        if self.status.is_possible(status):
            raise exc.Conflict(f'cannot change {self.status} -> {status}')

        self.status_actual.change(status, mps_code, mps_message, desc)
