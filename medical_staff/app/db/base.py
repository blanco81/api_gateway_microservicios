from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from app.config import settings

metadata = MetaData(schema=settings.DB_SCHEMA)
Base = declarative_base(metadata=metadata)

print(f"Base metada**: {Base.metadata.schema}")
