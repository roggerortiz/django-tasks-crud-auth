from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("auth/signup/", views.signup, name="signup"),
    path("auth/login/", views.signin, name="login"),
    path("auth/logout/", views.signout, name="logout"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<slug:slug>", views.edit_task, name="edit_task"),
    path("tasks/<slug:slug>/complete/", views.complete_task, name="complete_task"),
    path("tasks/<slug:slug>/delete/", views.delete_task, name="delete_task"),
]
