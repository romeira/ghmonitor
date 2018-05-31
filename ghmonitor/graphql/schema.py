import graphene
from api.graphql import schema as api_schema
from users.graphql import schema as users_schema


class Queries(api_schema.Query,
              users_schema.Query,
              graphene.ObjectType):
    pass


class Mutations(api_schema.Mutation,
                graphene.ObjectType):
    pass


schema = graphene.Schema(query=Queries, mutation=Mutations)
