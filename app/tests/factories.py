from uuid import UUID

from faker import Faker
from faker.providers import lorem, misc, person

from films.models import Film, Genre, Person, PersonRoles, PersonWithoutFilms

fake = Faker()

fake.add_provider(lorem)
fake.add_provider(misc)
fake.add_provider(person)


class GenreFactory:
    @classmethod
    def create(cls) -> Genre:
        return Genre(uuid=fake.uuid4(), name=fake.word())


class PersonFactory:
    @classmethod
    def create(cls) -> Person:
        return Person(
            uuid=fake.uuid4(),
            full_name=fake.name(),
            films=[PersonFactory.create_person_roles() for _ in range(fake.pyint(min_value=1, max_value=4))],
        )

    @classmethod
    def create_short(cls) -> PersonWithoutFilms:
        return PersonWithoutFilms(uuid=fake.uuid4(), full_name=fake.name())

    @staticmethod
    def create_person_roles() -> PersonRoles:
        return PersonRoles(uuid=fake.uuid4(), roles=[fake.word() for _ in range(fake.pyint(min_value=1, max_value=3))])


class FilmFactory:
    @classmethod
    def create(cls, uuid: UUID = None) -> Film:
        if uuid is None:
            uuid = fake.uuid4()

        return Film(
            uuid=uuid,
            title=fake.sentence(nb_words=fake.pyint(min_value=2, max_value=5)),
            imdb_rating=fake.pyfloat(left_digits=1, right_digits=1, positive=True, max_value=10),
            description=fake.paragraph(nb_sentences=fake.pyint(min_value=2, max_value=5)),
            genre=[GenreFactory.create() for _ in range(fake.pyint(min_value=1, max_value=3))],
            actors=[PersonFactory.create_short() for _ in range(fake.pyint(min_value=1, max_value=3))],
            writers=[PersonFactory.create_short() for _ in range(fake.pyint(min_value=1, max_value=3))],
            directors=[PersonFactory.create_short() for _ in range(fake.pyint(min_value=1, max_value=3))],
        )