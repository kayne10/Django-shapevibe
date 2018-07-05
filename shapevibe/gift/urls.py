from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'gift'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^profile/(?P<username>[\w|\W.-]+)/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit$', views.update_profile, name='update_profile'),
    url(r'^delete_user/(?P<username>[\w|\W.-]+)/$', views.delete_user, name='delete_user'),
    url(r'^(?P<gift_id>[0-9]+)/modal/$', views.modal, name='modal'),
    url(r'^(?P<gift_id>[0-9]+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<gift_id>[0-9]+)/edit/$', views.edit_gift, name='edit_gift'),
    url(r'^(?P<gift_id>[0-9]+)/delete/$', views.delete_gift, name='delete_gift'),
    url(r'^create_gift/$', views.create_gift, name='create_gift'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'registration/password_reset_form.html'}),
    url(r'^password_reset/done/$', auth_views.password_reset_done),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm),
    url(r'^reset/done/$', auth_views.password_reset_complete),
]