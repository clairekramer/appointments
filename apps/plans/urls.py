from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create$', views.create, name='create'),
    url(r'^(?P<app_id>\d+)$', views.edit, name='edit'),
    url(r'^(?P<app_id>\d+)/update$', views.update, name='update'),
    url(r'^(?P<app_id>\d+)/delete$', views.delete, name='delete')
]
