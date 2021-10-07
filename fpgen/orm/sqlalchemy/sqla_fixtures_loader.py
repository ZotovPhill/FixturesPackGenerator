import datetime
import json

from fpgen.orm.sqlalchemy.database import db
from fpgen.orm.abstract_fixtures_loader import AbstractFixturesLoader


class SQLAlchemyFixturesLoader(AbstractFixturesLoader):
    def load(self) -> None:
        pass

    def auto_load(self):
        if self.catalog:
            with open(self.catalog, "r") as response:
                items = json.loads(response.read())
                items = items[:self.quantity] if self.quantity else items
                objects = [self.model(**item) for item in items]
        else:
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

        self.save(objects)

    def save(self, objects: list):
        with db.session_scope() as session:
            session.bulk_save_objects(objects)
