import click
import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.federation import Schema
from strawberry.printer import print_schema

from graph_energy_scan.database import create_session
from graph_energy_scan.graphql import EnergyScan, Session

from . import __version__

__all__ = ["main"]

SCHEMA = Schema(types=[Session, EnergyScan], enable_federation_2=True)


@click.group(invoke_without_command=True)
@click.version_option(version=__version__)
def main():
    pass


@main.command()
@click.option("-p", "--path", type=str, help="The path to save the schema to")
def schema(path: str):
    sdl = print_schema(SCHEMA)
    if path:
        with open(path, "w") as outfile:
            outfile.write(sdl)
    else:
        print(sdl)


@main.command()
@click.option("--database-url", type=str, envvar="DATABASE_URL")
@click.option("--host", type=str, envvar="HOST", default="0.0.0.0")
@click.option("--port", type=int, envvar="PORT", default=80)
def serve(database_url: str, host: str, port: int):
    app = FastAPI()
    create_session(database_url)
    graphql_app = GraphQLRouter(SCHEMA)
    app.include_router(graphql_app, prefix="/graphql")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
