from django.conf.urls import url

from . import views

app_name = 'gift'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^(?P<gift_id>[0-9]+)/$', views.detail, name='detail'),
]