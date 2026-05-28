from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker, Query


_Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))


class BaseModel(_Base):
    __abstract__ = True

    __tablename__ = None
    __table_args__ = None
    query = db_session.query_property()  # type: Query


def configure(dsn: str, pool_size: int = 100, max_overflow: int = 20,  echo: bool = False):
    from internal.models import catalog, identity, processing, risk, vault  # noqa

    engine = create_engine(dsn, echo=echo, pool_size=pool_size, max_overflow=max_overflow)
    db_session.configure(bind=engine)

    return engine
