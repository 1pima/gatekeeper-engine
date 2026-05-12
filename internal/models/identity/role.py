from sqlalchemy import Column, String, BigInteger
from sqlalchemy_utils import ChoiceType

from internal.const.rbac import RoleName
from internal.models.base import BaseModel


class Role(BaseModel):
    """
    Роли пользователей: many-to-many через *users_roles*
    """
    __tablename__ = 'role'
    __table_args__ = {'schema': 'identity'}

    id = Column(BigInteger, primary_key=True)
    name = Column(ChoiceType(RoleName, impl=String()), nullable=False)
    description = Column(String(255))

    def __repr__(self):
        return f'<Role #{self.id} [{self.name}]>'
