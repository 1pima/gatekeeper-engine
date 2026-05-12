from internal.util import dbc


class BaseModel(dbc.Model):
    __abstract__ = True

    __tablename__ = None
    __table_args__ = {'schema': None}
