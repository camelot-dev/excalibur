from ..settings import engine


def initialize_database():
    from ..models import Base

    Base.metadata.create_all(engine)


def reset_database():
    from ..models import Base

    Base.metadata.drop_all(engine)
    initialize_database()