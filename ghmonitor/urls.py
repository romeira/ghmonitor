from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

import django_js_reverse.views

from api.graphql.views import GraphQLView
from api.rest.routers import router as rest_router


index_view = TemplateView.as_view(template_name='api/index.html')
login_view = TemplateView.as_view(template_name='auth/login.html')
logout_view = auth_views.logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),

    url(r'^$', login_required(index_view), name='index'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),

    url('^oauth/', include('social_django.urls', namespace='social')),

    url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
    url(r'^rest/', include(rest_router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
