from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^prepare_deploy/$',views.prepare_deploy,name='prepare_deploy'),
    url(r'^check_confirm/$',views.check_confirm,name='check_confirm'),
    url(r'^deploy/$',views.deploy,name='deploy'),
]
