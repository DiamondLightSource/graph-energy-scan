import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def hello() -> str:
        return "Hello World"
