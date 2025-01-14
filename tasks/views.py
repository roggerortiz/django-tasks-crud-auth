from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .utils import string_to_slug
from .forms import CreateTask
from .models import Task


# Create your views here.
def home(request):
    return render(request, "pages/index.html")


def signup(request):
    if request.method == "GET":
        return render(request, "pages/auth/signup.html", {"form": UserCreationForm()})
    else:
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(
                request,
                "pages/auth/signup.html",
                {"form": UserCreationForm(), "error": "Passwords do not match"},
            )

        try:
            user = User.objects.create(username=username, password=password1)
            login(request, user)
            return redirect("tasks")
        except IntegrityError:
            return render(
                request,
                "pages/auth/signup.html",
                {"form": UserCreationForm(), "error": "User already exists"},
            )


def signin(request):
    if request.method == "GET":
        return render(request, "pages/auth/signin.html", {"form": AuthenticationForm()})
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(
                request,
                "pages/auth/signin.html",
                {
                    "form": AuthenticationForm(),
                    "error": "Username or password is incorrect",
                },
            )

        login(request, user)
        return redirect("tasks")


def signout(request):
    logout(request)
    return redirect("home")


def tasks(request):
    tasks = Task.objects.all()
    return render(request, "pages/tasks/index.html", {"tasks": tasks})


def task_details(request, slug):
    task = get_object_or_404(Task, slug=slug)
    return render(request, "pages/tasks/details.html", {"task": task})


def create_task(request):
    if request.method == "GET":
        return render(
            request,
            "pages/tasks/create.html",
            {"form": CreateTask()},
        )
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        user = request.POST.get("user")
        print(request.POST)
        Task.objects.create(
            title=title,
            slug=string_to_slug(title),
            description=description,
            user_id=user,
        )
        return redirect("tasks")


def complete_task(request):
    if request.method == "GET":
        return Http404()
    else:
        id = request.POST.get("id")
        task = get_object_or_404(Task, id=id)
        task.completed = not task.completed
        task.save()

        return redirect("tasks")


def delete_task(request):
    if request.method == "GET":
        return Http404()
    else:
        id = request.POST.get("id")
        task = get_object_or_404(Task, id=id)
        task.delete()

        return redirect("tasks")
