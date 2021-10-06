import random

from fpgen.example.models.goods import Product, Unit, Category
from fpgen.abstract_fixture_loader import AbstractFixtureLoader

from fpgen.example.database import db


class LoadGoods(AbstractFixtureLoader):
    def load(self) -> None:
        with db.session_scope() as session:
            units = session.query(Unit).all()
            categories = session.query(Category).all()
            units_count = len(units)
            categories_count = len(categories)
            objects = [
                Product(
                    name=self.fake.sentence(nb_words=4, variable_nb_words=True),
                    country_of_origin=self.fake.country_code(),
                    expiration_time=self.fake.date_between(start_date='today', end_date='+10y'),
                    unit_id=units[random.randint(0, units_count-1)].id,
                    category_id=categories[random.randint(0, categories_count-1)].id
                )
                for _ in range(self.quantity)
            ]
            session.bulk_save_objects(objects)

    @staticmethod
    def env_group() -> list:
        return ['dev', 'prod']
