from abstract_fixture_loader import AbstractFixtureLoader
from fpgen.example.models.goods import Unit


class LoadUnit(AbstractFixtureLoader):
    __model__ = Unit

    @staticmethod
    def env_group() -> list:
        return ['dev', 'prod']
