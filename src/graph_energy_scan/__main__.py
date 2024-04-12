from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from graph_energy_scan.graphql import Query

from . import __version__

__all__ = ["main"]


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args(args)

    app = FastAPI()
    schema = Schema(Query)
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")
    uvicorn.run(app)


if __name__ == "__main__":
    main()
