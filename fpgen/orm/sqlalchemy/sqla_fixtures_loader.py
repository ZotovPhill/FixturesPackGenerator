import datetime
import json
from typing import Optional

from fpgen.orm.sqlalchemy.sqla_database import SQLAlchemyDatabase
from fpgen.orm.abstract_fixtures_loader import AbstractFixturesLoader


class SQLAlchemyFixturesLoader(AbstractFixturesLoader):
    def __init__(self, db_url: Optional[str] = None):
        self.db = SQLAlchemyDatabase(db_url)
        super().__init__()

    def load(self) -> None:
        pass

    def auto_load(self) -> None:
        objects = self.auto_load_from_catalog() \
            if self.catalog \
            else self.auto_load_from_model()
        self.save(objects)

    def auto_load_from_catalog(self) -> list:
        with open(self.catalog, "r") as response:
            items = json.loads(response.read())
            items = items[:self.quantity] if self.quantity else items
            return [self.model(**item) for item in items]

    def auto_load_from_model(self) -> list:
        objects = []
        for _ in range(self.quantity):
            entity_obj = self.model()
            for column in self.model.__table__.columns:
                column_name, column_type = column.name, column.type
                if column_name == "id":
                    continue
                if issubclass(column_type.python_type, str):
                    value = self.fake.sentence(nb_words=4, variable_nb_words=True)
                elif issubclass(column_type.python_type, (int, float)):
                    value = self.fake.pyfloat(positive=True, max_value=1000000)
                elif issubclass(column_type.python_type, datetime.datetime):
                    value = self.fake.date_time_between(start_date='-10y', end_date='+10y'),
                else:
                    value = None
                setattr(entity_obj, column_name, value)
            objects.append(entity_obj)

        return objects

    def save(self, objects: list) -> None:
        with self.db.session_scope() as session:
            session.bulk_save_objects(objects)
