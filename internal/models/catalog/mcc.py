from sqlalchemy import Column, String, BigInteger
from sqlalchemy_utils import ChoiceType

from internal.const.rbac import RoleName
from internal.models.base import BaseModel


class MCC(BaseModel):
    """
    Merchant Category Code
    """
    __tablename__ = 'mcc'
    __table_args__ = {'schema': 'catalog'}

    id = Column(BigInteger, primary_key=True)
    code_name = Column(ChoiceType(RoleName, impl=String()), nullable=False)

    def __repr__(self):
        return f'<MCC #{self.id} [{self.code_name}]>'
