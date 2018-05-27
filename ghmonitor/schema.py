import graphene

import api.schema
import users.schema


class Query(api.schema.Query,
            users.schema.Query,
            graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
