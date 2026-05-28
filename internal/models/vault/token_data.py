from sqlalchemy import Column, String, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from ..base import BaseModel


class TokenData(BaseModel):
    """
    """

    __tablename__ = 'token'
    __table_args__ = {'schema': 'vault'}

    id = Column(BigInteger, primary_key=True)
    dpan = Column(String, nullable=False)
    exp_date = Column(String, nullable=False)
    encrypted_dek_key = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    mask = Column(String, nullable=False)
    is_blocked = Column(Boolean, default=False)
    description = Column(String)

    user_id = Column(BigInteger, ForeignKey('identity.user.id'), nullable=False)
    user = relationship('User', back_populates='tokens')

    card_id = Column(BigInteger, ForeignKey('vault.card.id'), nullable=False)
    card = relationship('CardData', back_populates='tokens')

    transactions = relationship('Transaction', back_populates='token')
    limits = relationship('Limits', back_populates='token')
    accumulators = relationship('Accumulator', back_populates='token')

    def __repr__(self):
        return f'<Token #{self.id} [{self.mask}/{self.hash}]>'
