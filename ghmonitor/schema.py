import graphene

import api.schema
import users.schema


class Queries(api.schema.Query,
              users.schema.Query,
              graphene.ObjectType):
    pass


class Mutations(api.schema.Mutation,
                graphene.ObjectType):
    pass


schema = graphene.Schema(query=Queries, mutation=Mutations)
