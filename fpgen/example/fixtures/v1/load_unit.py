import json

from abstract_fixture_loader import AbstractFixtureLoader
from fpgen.example.database import db
from fpgen.example.models.goods import Unit


class LoadUnit(AbstractFixtureLoader):
    def load(self) -> None:
        with open(self.catalog, "r") as response:
            units = json.loads(response.read())
            units = units[:self.quantity] if self.quantity else units
            objects = [Unit(**unit) for unit in units]
            with db.session_scope() as session:
                session.bulk_save_objects(objects)

    @staticmethod
    def env_group() -> list:
        return ['dev', 'prod']
