from sqlmodel import create_engine, Session, SQLModel

# Create the SQLite database engine
engine = create_engine(
    "sqlite:///./backend/pony_express.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def reset_db_and_tables():
    SQLModel.metadata.drop_all(engine)  # Drop all tables
    SQLModel.metadata.create_all(engine)  # Recreate all tables


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    reset_db_and_tables()
