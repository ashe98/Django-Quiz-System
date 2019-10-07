from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.user_login, name = 'login'),
    url(r'^home', views.home, name = 'home'),
    url(r'^result', views.questions, name = 'result'),
    url(r'^addqn', views.addqn, name = 'addqn'),
    url(r'^logout', views.user_logout, name = 'logout'),
    url(r'^create', views.createquiz, name = 'create_quiz'),
    url(r'^viewres', views.select, name = 'viewres'),
    url(r'^takequiz', views.takequiz, name = 'take_quiz'),
    url(r'^res/(?P<quiz_name>[\w]+)', views.score, name = 'score'),
    url(r'^(?P<quiz_name>[\w]+)', views.questions, name = 'questions'),

    
]
