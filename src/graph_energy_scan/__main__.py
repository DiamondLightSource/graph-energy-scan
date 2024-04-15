import click
import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.federation import Schema
from strawberry.printer import print_schema

from graph_energy_scan.database import create_session
from graph_energy_scan.graphql import EnergyScan, Query, Session

from . import __version__

__all__ = ["main"]


@click.group(invoke_without_command=True)
@click.version_option(version=__version__)
def main():
    pass


@main.command()
@click.option("-p", "--path", type=str, help="The path to save the schema to")
def schema(path: str):
    schema = Schema(Query, types=[Session, EnergyScan], enable_federation_2=True)
    sdl = print_schema(schema)
    if path:
        with open(path, "w") as outfile:
            outfile.write(sdl)
    else:
        print(sdl)


@main.command()
@click.argument("database-url", type=str)
def serve(database_url: str):
    app = FastAPI()
    schema = Schema(Query, types=[Session, EnergyScan], enable_federation_2=True)
    create_session(database_url)
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")
    uvicorn.run(app)


if __name__ == "__main__":
    main()
