from fpgen.abstract_fixture_loader import AbstractFixtureLoader
from fpgen.example.database import db
from fpgen.example.models.goods import Category


class LoadCategory(AbstractFixtureLoader):
    def load(self) -> None:
        objects = [
            Category(
                name=self.fake.sentence(nb_words=4, variable_nb_words=True),
                description=self.fake.sentence(nb_words=4, variable_nb_words=True)
            )
            for _ in range(self.quantity)
        ]
        with db.session_scope() as session:
            session.bulk_save_objects(objects)

    @staticmethod
    def env_group() -> list:
        return ['dev', 'prod']
