import asyncio
import os

import setuptools
from sqlacodegen_v2.generators import DeclarativeGenerator
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine


async def generate_models():
    engine = create_async_engine(os.environ["DATABASE_URL"])
    metadata = MetaData()
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda connection: metadata.reflect(connection, only=["EnergyScan"])
        )
        generator = await connection.run_sync(
            lambda connection: DeclarativeGenerator(metadata, connection, set())
        )
    with open("src/graph_energy_scan/models.py", "w") as models_file:
        models_file.write(generator.generate())


if __name__ == "__main__":
    asyncio.run(generate_models())
    setuptools.setup()
