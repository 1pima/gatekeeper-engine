from datetime import datetime

from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, Numeric, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from ..base import BaseModel
from ..catalog import MCC
from ..vault import TokenData
from ...const.internal import LimitPeriodType


class Limits(BaseModel):
    """
    """
    __tablename__ = 'limits'
    __table_args__ = {'schema': 'risk'}

    id = Column(BigInteger, primary_key=True)
    amount = Column(Numeric(15, 2), nullable=False)
    date_start = Column(DateTime, default=datetime.utcnow())
    date_end = Column(DateTime, default=datetime.utcnow())
    period_type = Column(ChoiceType(LimitPeriodType, impl=Integer()), nullable=False)

    mcc_id = Column(BigInteger, ForeignKey(MCC.id), nullable=False)
    mcc = relationship(MCC, back_populates='limit', overlaps='limit', uselist=False)

    token_id = Column(BigInteger, ForeignKey(TokenData.id), nullable=False)
    token = relationship(TokenData, back_populates='limit', overlaps='limit', uselist=False)

    def __repr__(self):
        return f'<Limit {self.amount}KZT {self.MCC} [{self.date_start.date} - {self.date_end.date}] of {self.token}>'
