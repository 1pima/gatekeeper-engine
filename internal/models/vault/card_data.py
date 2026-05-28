from sqlalchemy import Column, String, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from ..base import BaseModel


class CardData(BaseModel):
    """
    Пользователи, связь с ролями: many-to-many через *users_roles*
    """

    __tablename__ = 'card'
    __table_args__ = {'schema': 'vault'}

    id = Column(BigInteger, primary_key=True)
    pan = Column(String, nullable=False)
    exp_date = Column(String, nullable=False)
    encrypted_dek_key = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    mask = Column(String, nullable=False)
    is_blocked = Column(Boolean, default=False)
    description = Column(String)

    user_id = Column(BigInteger, ForeignKey('identity.user.id'), nullable=False)
    user = relationship('User', back_populates='cards')

    tokens = relationship('TokenData', back_populates='card')

    def __repr__(self):
        return f'<Card #{self.id} [{self.mask}/{self.hash}]>'
