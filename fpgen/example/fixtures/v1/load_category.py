from fpgen.abstract_fixture_loader import AbstractFixtureLoader
from fpgen.example.models.goods import Category


class LoadCategory(AbstractFixtureLoader):
    __model__ = Category

    @staticmethod
    def env_group() -> list:
        return ['dev', 'prod']
