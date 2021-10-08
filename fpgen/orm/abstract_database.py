class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    def truncate_database(self) -> None:
        raise NotImplementedError()

    def drop_database(self) -> None:
        raise NotImplementedError()

    def create_database(self) -> None:
        raise NotImplementedError()
