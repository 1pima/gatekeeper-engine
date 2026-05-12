from sqlalchemy import Column, BigInteger, ForeignKey

from internal.models.base import BaseModel


class UsersRoles(BaseModel):

    __tablename__ = 'users_roles'
    __table_args__ = {'schema': 'identity'}

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('identity.user.id'))
    role_id = Column(BigInteger, ForeignKey('identity.role.id'))
