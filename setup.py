import os

import setuptools
from sqlacodegen_v2.generators import DeclarativeGenerator
from sqlalchemy import MetaData, create_engine

if __name__ == "__main__":
    engine = create_engine(os.environ["DATABASE_URL"])
    metadata = MetaData()
    metadata.reflect(engine, only=["EnergyScan"])
    generator = DeclarativeGenerator(metadata, engine, set())
    with open("src/graph_energy_scan/models.py", "w") as models_file:
        models_file.write(generator.generate())
    setuptools.setup()
