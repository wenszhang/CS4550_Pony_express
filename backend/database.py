import os

from sqlmodel import create_engine, Session, SQLModel

# Check the environment variable
if os.environ.get("DB_LOCATION") == "EFS":
    db_path = "/mnt/efs/pony_express.db"
    echo = False
else:
    db_path = "pony_express.db"
    echo = True

# Create the SQLite database engine
engine = create_engine(
    f"sqlite:///{db_path}",
    echo=echo,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
