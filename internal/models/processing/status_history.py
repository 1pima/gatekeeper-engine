from sqlalchemy import Column, String, BigInteger, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from .transaction import Transaction
from ..base import BaseModel
from ..vault import TokenData
from ...const.transaction import TransactionStatus


class StatusHistory(BaseModel):
    """
    Данные о транзакции iso8583
    """
    __tablename__ = 'status_history'
    __table_args__ = {'schema': 'processing'}

    id = Column(BigInteger, primary_key=True)
    is_actual = Column(Boolean, default=True)
    status = Column(ChoiceType(TransactionStatus, impl=Integer()), nullable=False)
    code = Column(String)
    message = Column(String)
    description = Column(String)

    transaction_id = Column(BigInteger, ForeignKey(Transaction.id), nullable=False)
    transaction = relationship(TokenData, back_populates='status', overlaps='status', uselist=False)

    def __repr__(self):
        return f'<Status of #{self.transaction_id} [{self.status}]>'
