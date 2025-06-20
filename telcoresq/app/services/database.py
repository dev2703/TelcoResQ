import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float, Text

def get_engine(db_url):
    """Creates a SQLAlchemy engine."""
    return create_engine(db_url)

def create_tables(engine):
    """Creates all necessary tables in the database."""
    metadata = MetaData()

    survey_responses = Table('survey_responses', metadata,
        Column('response_id', Integer, primary_key=True, autoincrement=True),
        Column('processed_text', Text, nullable=False),
        Column('sentiment_score', Float),
        Column('sentiment_label', String(50))
    )

    embeddings = Table('embeddings', metadata,
        Column('embedding_id', Integer, primary_key=True, autoincrement=True),
        Column('response_id', Integer, sqlalchemy.ForeignKey('survey_responses.response_id')),
        Column('vector', Text, nullable=False) # Storing as text for simplicity, will be JSON/bytes in practice
    )

    themes = Table('themes', metadata,
        Column('theme_id', Integer, primary_key=True, autoincrement=True),
        Column('theme_name', String(255), unique=True, nullable=False),
        Column('frequency', Integer, default=1),
        Column('examples', Text) # Storing as JSON string
    )

    metadata.create_all(engine)
    print("Tables created successfully.") 