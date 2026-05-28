from sqlalchemy import Column, String, BigInteger, ForeignKey, Integer, Boolean, Uuid
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

    transaction_id = Column(Uuid, ForeignKey('processing.transaction.id'), nullable=False)
    transaction = relationship('Transaction', back_populates='status_history')

    def __repr__(self):
        return f'<Status of #{self.transaction_id} [{self.status}]>'

    @classmethod
    def create(cls, status, code, message, transaction_id, desc=None):
        state = cls()
        state.status = status
        state.code = code
        state.message = message
        state.transaction_id = transaction_id

        if desc:
            state.description = desc

        cls.query.session.add(state)
        cls.query.session.commit()

    def change(self, status, code, message, desc=None):
        # делаем данную запись более неактуальной
        self.is_actual = False
        self.query.session.commit()

        # создаем новую
        self.create(status, code, message, self.transaction_id, desc)
