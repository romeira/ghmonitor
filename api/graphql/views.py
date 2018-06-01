from django.contrib.auth.mixins import LoginRequiredMixin

from graphene_django.views import GraphQLView as _GraphQLView


class GraphQLView(LoginRequiredMixin, _GraphQLView):
    pass
