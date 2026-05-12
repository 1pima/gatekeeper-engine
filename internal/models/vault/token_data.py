from sqlalchemy import Column, String, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from ..base import BaseModel
from ..identity import User, Organization


class TokenData(BaseModel):
    """
    Пользователи, связь с ролями: many-to-many через *users_roles*
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

    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    user = relationship(Organization, back_populates='token', overlaps='token', uselist=False)

    card_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    card = relationship(Organization, back_populates='token', overlaps='token', uselist=False)

    def __repr__(self):
        return f'<Token #{self.id} [{self.mask}/{self.hash}]>'
