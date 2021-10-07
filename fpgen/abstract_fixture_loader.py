import datetime
import json
import faker

from fpgen.example.database import db


class Meta(type):
    def __new__(cls, name, bases, attrs):
        newattrs = {}
        for attrname, attrvalue in attrs.items():
            if attrname in ["__quantity__", "__catalog__", "__model__"]:
                newattrs[attrname.removesuffix("__").removeprefix("__")] = attrvalue
            else:
                newattrs[attrname] = attrvalue

        return super().__new__(cls, name, bases, newattrs)


class AbstractFixtureLoader(metaclass=Meta):
    """
    Values from .yaml config file has priority over default attributes.
    Leave "attributes:" empty to use dunder attributes.

    __catalog__ = "fpgen/example/fixtures/catalog/v1/unit_list.json"
    __quantity__ = 20
    """

    quantity = None
    catalog = None
    model = None

    def __init__(self):
        self.fake = faker.Faker()

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

        with db.session_scope() as session:
            session.bulk_save_objects(objects)

    @staticmethod
    def env_group() -> list:
        return []
