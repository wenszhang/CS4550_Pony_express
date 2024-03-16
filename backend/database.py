from sqlmodel import create_engine, Session, SQLModel
from .schema import UserInDB, ChatInDB, MessageInDB, UserChatLinkInDB

# Create the SQLite database engine
engine = create_engine(
    "sqlite:///./backend/pony_express.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
