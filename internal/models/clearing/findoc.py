from sqlalchemy import Column, BigInteger
from sqlalchemy.dialects.postgresql import JSONB

from ..base import BaseModel


class FinancialDocument(BaseModel):
    """
    TODO
    """
    __tablename__ = 'fin_doc'
    __table_args__ = {'schema': 'clearing'}

    id = Column(BigInteger, primary_key=True)
    add_info = Column(JSONB, default={})

    def __repr__(self):
        return f'<FinDoc #{self.id} [null]>'
