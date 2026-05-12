from datetime import datetime

from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime, Numeric, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from ..base import BaseModel
from ..catalog import MCC
from ..vault import TokenData
from ...const.iso8583 import TransactionType
from ...const.transaction import Currency


class Transaction(BaseModel):
    """
    Данные о транзакции iso8583
    """
    __tablename__ = 'transaction'
    __table_args__ = {'schema': 'processing'}

    id = Column(BigInteger, primary_key=True)
    reference = Column(String, nullable=False)
    ext_id = Column(String, nullable=False)
    type = Column(ChoiceType(TransactionType, impl=String()), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow())
    authorized_at = Column(DateTime, nullable=True)

    transaction_amount = Column(Numeric(15, 2), nullable=False)
    transaction_currency = Column(ChoiceType(Currency, impl=Integer()), nullable=False)
    settlement_amount = Column(Numeric(15, 2), nullable=False)
    settlement_currency = Column(ChoiceType(Currency, impl=Integer()), nullable=False)
    bank_data = Column(JSONB, default={})
    add_info = Column(JSONB, default={})

    token_id = Column(BigInteger, ForeignKey(TokenData.id), nullable=False)
    token = relationship(TokenData, back_populates='transaction', overlaps='transaction', uselist=False)

    mcc_id = Column(BigInteger, ForeignKey(MCC.id), nullable=False)
    mcc = relationship(MCC, back_populates='transaction', overlaps='transaction', uselist=False)

    status_history = relationship('StatusLog', primaryjoin="Order.iid==foreign(StatusLog.transaction_id)",
                                  lazy='dynamic', uselist=True, viewonly=True)
    status_actual = relationship(
        'StatusLog',
        primaryjoin="and_(foreign(Transaction.id)==StatusHistory.transaction_id, StatusHistory.is_actual.is_(True))",
        uselist=False,
        lazy='joined'
    )
    status = association_proxy('status_actual', 'status')

    def __repr__(self):
        return f'<Transaction #{self.id} [{self.reference}/{self.ext_id}]>'
