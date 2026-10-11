from sqlalchemy import create_engine, text
from models import Base

DATABASE_URL = "postgresql+psycopg://postgres:Ceratophyllun98@localhost:5432/aplhadb"

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.scalar())

Base.metadata.create_all(engine)