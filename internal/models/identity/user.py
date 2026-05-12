from datetime import datetime

from sqlalchemy import Column, DateTime, String, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref

from .organization import Organization
from ..base import BaseModel
from .users_roles import UsersRoles


class User(BaseModel):
    """
    Пользователи, связь с ролями: many-to-many через *users_roles*
    """

    __tablename__ = 'user'
    __table_args__ = {'schema': 'identity'}

    id = Column(BigInteger, primary_key=True)
    username = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    is_active = Column(Boolean(), default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    # organization
    organization_id = Column(BigInteger, ForeignKey(Organization.id), nullable=False)
    organization = relationship(Organization, back_populates='user', overlaps='user', uselist=False)
    # rbac
    roles = relationship('Role', secondary=UsersRoles.__table__, backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<Organization #{self.id} [{self.username}/{self.email}]>'
