import graphene
from graphene_django.types import DjangoObjectType

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        only_fields = ('username',)
        model = User


class Query:
    user = graphene.Field(UserType)

    def resolve_user(self, info, **kwargs):
        user = info.context.user
        return user if user.is_authenticated else None
