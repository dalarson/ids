from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from faker import Faker


class LocalDatabase():
    def __init__(self):
        self.users = []
        self.id = 0
        # load 1000 fake shits
        fake = Faker()
        for _ in range(1000):
            self.add_user(fake.name(), fake.ssn())

    def add_user(self, name, ssn):
        self.users.append(
            {"name": name,  "ssn": ssn, "id": self.id}
        )
        self.id += 1

    def get_user_by_name(self, name):
        matching_users = [u for u in self.users if u['name'] == name]
        if len(matching_users) != 1:
            return None
        return matching_users[0]

    def get_user_by_id(self, uid):
        for u in self.users:
            if u['id'] == uid:
                return u
        return None


Base = declarative_base()


class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ssn = Column(String)


class RemoteDatabase():
    def __init__(self, host="10.0.0.2", user="postgres", password="admin", database="postgres"):
        db_uri = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
            user, password, host, database)
        self.engine = create_engine(db_uri)
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)

    def add_user(self, name, ssn):
        self.session.add(Person(name=name, ssn=ssn))
        self.session.commit()

    def get_user_by_name(self, name):
        return self.session.query(Person).filter_by(name=name).one()

    def get_user_by_id(self, uid):
        return self.session.query(Person).filter_by(id=uid).one()
