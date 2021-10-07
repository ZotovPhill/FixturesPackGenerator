from abc import abstractmethod

import faker


class Meta(type):
    def __new__(cls, name, bases, attrs):
        newattrs = {}
        for attrname, attrvalue in attrs.items():
            if attrname in ["__quantity__", "__catalog__", "__model__"]:
                newattrs[attrname.removesuffix("__").removeprefix("__")] = attrvalue
            else:
                newattrs[attrname] = attrvalue

        return super().__new__(cls, name, bases, newattrs)


class AbstractFixturesLoader(metaclass=Meta):
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

    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def auto_load(self):
        pass

    @abstractmethod
    def save(self, objects: list):
        pass

    @staticmethod
    def env_group() -> list:
        return []
