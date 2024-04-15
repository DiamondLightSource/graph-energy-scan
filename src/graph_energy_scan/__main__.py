import click
import uvicorn
from fastapi import FastAPI
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from graph_energy_scan.database import create_session
from graph_energy_scan.graphql import Query

from . import __version__

__all__ = ["main"]


@click.group(invoke_without_command=True)
@click.version_option(version=__version__)
@click.argument("database-url", type=str)
def main(database_url: str):
    app = FastAPI()
    schema = Schema(Query)
    create_session(database_url)
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")
    uvicorn.run(app)


if __name__ == "__main__":
    main()
