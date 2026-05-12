from datetime import datetime

from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, Numeric, Integer
from sqlalchemy.orm import relationship

from ..base import BaseModel
from ..vault import TokenData


class Accumulator(BaseModel):
    __tablename__ = 'accumulator'
    __table_args__ = {'schema': 'risk'}

    id = Column(BigInteger, primary_key=True)
    current_amount = Column(Numeric(15, 2), nullable=False)
    current_count = Column(BigInteger, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow())
    reset_at = Column(DateTime)
    updated_at = Column(DateTime)

    version = Column(Integer, default=1)

    token_id = Column(BigInteger, ForeignKey(TokenData.id), nullable=False)
    token = relationship(TokenData, back_populates='limit', overlaps='limit', uselist=False)

    def __repr__(self):
        return f'<Accumulator {self.current_amount}KZT {self.current_count}x [{self.token}]>'
