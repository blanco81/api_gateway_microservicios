import os
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, text
from alembic import context
from app.config import settings
from app.model.models import Base



# 1) Ajusta el path para que 'app' sea importable
# Agrega la ruta a sys.path para poder importar config.py
sys.path.append(str(Path(__file__).resolve().parents[1]))



# 2) Configuración de Alembic
config = context.config
fileConfig(config.config_file_name)

# 3) URL de conexión SÍNCRONA para Alembic
SYNC_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_DATABASE}"
)
config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

# 4) Usamos el metadata de Base, no un MetaData vacío
target_metadata = Base.metadata

print(f"Base metada****: {Base.metadata}")

# 5) Solo incluimos objetos del esquema correcto
#def include_object(object, name, type_, reflected, compare_to):
#    if type_ == "table":
#        return object.schema == settings.DB_SCHEMA
#    return True

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        #include_object=include_object,
        version_table_schema=target_metadata.schema
    )
    with context.begin_transaction():
        context.run_migrations()
        
print("Tablas encontradas en metadata:")
for t in target_metadata.tables.values():
    print(f"- {t.name} (schema: {t.schema})")

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)
    
    with connectable.connect() as connection:
        #print("✅ Conectado a DB:", connection.engine.url) 
        # Verifica que el esquema existe
        #result = connection.execute(text(
        #    "SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema"
        #), {"schema": settings.DB_SCHEMA})
        #print(f"Esquema existe?: {'Sí' if result.fetchone() else 'No'}")
        #connection.execute(f"CREATE SCHEMA IF NOT EXISTS {settings.DB_SCHEMA}")

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=target_metadata.schema,
            include_schemas=True
        )
        
        
        with context.begin_transaction():
            print("🚀 Ejecutando migraciones...")
            context.execute(f"CREATE SCHEMA IF NOT EXISTS {settings.DB_SCHEMA}")
            context.execute(text(f'SET search_path TO {settings.DB_SCHEMA}'))
            context.run_migrations()
            print("✅ Migraciones completadas.")

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
