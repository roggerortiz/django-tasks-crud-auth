from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/complete/", views.complete_task, name="complete_task"),
    path("tasks/delete/", views.delete_task, name="delete_task"),
    path("tasks/<str:slug>/", views.task_details, name="task_details"),
]
