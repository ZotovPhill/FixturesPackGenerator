import contextlib
import os
from collections import Callable
from contextlib import contextmanager, AbstractContextManager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from fpgen.orm.sqlalchemy.base import Base


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )
        self.create_database()

    def truncate_database(self) -> None:
        with contextlib.closing(self._engine.connect()) as con:
            trans = con.begin()
            for table in reversed(Base.sorted_tables):
                con.execute(table.delete())
            trans.commit()

    def drop_database(self) -> None:
        Base.metadata.drop_all(self._engine)

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session_scope(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


db = Database(os.environ['DATABASE_URL'])
