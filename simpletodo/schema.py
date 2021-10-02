import graphene
import todo.schema


class Query(todo.schema.Query, graphene.ObjectType):
    """Query object."""

schema = graphene.Schema(query=Query)
