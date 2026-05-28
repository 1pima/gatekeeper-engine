from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import BigInteger, String

from internal.models.base import BaseModel


class Organization(BaseModel):
    """
    Таблица организаций партнеров
    """
    __tablename__ = 'organization'
    __table_args__ = {'schema': 'identity'}

    id = Column(BigInteger, primary_key=True)
    bin = Column(String(12))
    name = Column(String(255))
    users = relationship('User', back_populates='organization')

    def __repr__(self):
        return f'<Organization #{self.id} {self.name} [{self.bin}] >'
