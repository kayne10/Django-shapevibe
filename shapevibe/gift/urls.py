from django.conf.urls import url

from . import views

app_name = 'gift'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^profile/(?P<username>[\w|\W.-]+)/$', views.view_profile, name='view_profile'),
    # url(r'^(?P<username>[\w|\W.-]+)/$', views.view_profile_gifts, name='view_profile_gifts'),
    url(r'^profile/edit$', views.update_profile, name='update_profile'),
    url(r'^delete_user/(?P<username>[\w|\W.-]+)/$', views.delete_user, name='delete_user'),
    url(r'^(?P<gift_id>[0-9]+)/modal/$', views.modal, name='modal'),
    url(r'^(?P<gift_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<gift_id>[0-9]+)/edit/$', views.edit_gift, name='edit_gift'),
    url(r'^(?P<gift_id>[0-9]+)/delete/$', views.delete_gift, name='delete_gift'),
    url(r'^create_gift/$', views.create_gift, name='create_gift'),
]