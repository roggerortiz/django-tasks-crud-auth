from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.utils import timezone
from .forms import SignUpForm, SignInForm, TaskForm
from .models import Task


# Create your views here.
def home(request):
    return render(request, "pages/index.html")


def signup(request):
    if request.method == "GET":
        return render(request, "pages/auth/signup.html", {"form": SignUpForm()})
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        form = SignUpForm(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "username": username,
                "password1": password1,
                "password2": password2,
            }
        )

        if password1 != password2:
            form.non_field_errors = ["Passwords do not match"]
            return render(request, "pages/auth/signup.html", {"form": form})

        if not form.is_valid():
            return render(request, "pages/auth/signup.html", {"form": form})

        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=make_password(password1),
            )

            login(request, user)
            return redirect("tasks")
        except IntegrityError:
            form.non_field_errors = ["User already exists"]
            return render(request, "pages/auth/signup.html", {"form": form})


def signin(request):
    if request.method == "GET":
        return render(request, "pages/auth/login.html", {"form": SignInForm()})
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        form = SignInForm(
            {
                "username": username,
                "password": password,
            }
        )

        if not form.is_valid():
            return render(request, "pages/auth/login.html", {"form": form})

        user = authenticate(request, username=username, password=password)

        if user is None:
            form.non_field_errors = ["Username or password is incorrect"]
            return render(request, "pages/auth/login.html", {"form": form})

        login(request, user)
        return redirect("tasks")


def signout(request):
    logout(request)
    return redirect("home")


@login_required
def tasks(request):
    completed = request.GET.get("completed")

    if completed is not None:
        completed_at_is_null = completed == "false"
        tasks = Task.objects.filter(
            user=request.user, completed_at__isnull=completed_at_is_null
        ).order_by("-completed_at")
    else:
        tasks = Task.objects.filter(user=request.user).order_by("-created_at")

    return render(
        request, "pages/tasks/index.html", {
            "tasks": tasks, "completed": completed}
    )


@login_required
def create_task(request):
    if request.method == "GET":
        return render(
            request,
            "pages/tasks/form.html",
            {"form": TaskForm()},
        )
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        important = request.POST.get("important")

        form = TaskForm(
            {
                "title": title,
                "description": description,
                "important": important,
            }
        )

        if not form.is_valid():
            return render(request, "pages/tasks/form.html", {"form": form})

        Task.objects.create(
            title=title,
            slug=slugify(title),
            description=description,
            important=important is not None,
            user=request.user,
        )

        return redirect("tasks")


@login_required
def edit_task(request, slug):
    task = get_object_or_404(Task, slug=slug)

    if request.method == "GET":
        form = TaskForm(
            {
                "title": task.title,
                "description": task.description,
                "important": task.important,
            }
        )

        return render(request, "pages/tasks/form.html", {"task": task, "form": form})
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        important = request.POST.get("important")

        form = TaskForm(
            {
                "title": title,
                "description": description,
                "important": important,
            }
        )

        if not form.is_valid():
            return render(
                request, "pages/tasks/form.html", {"task": task, "form": form}
            )

        task.title = title
        task.description = description
        task.important = important is not None
        task.save()

        return redirect("tasks")


@login_required
def complete_task(request, slug):
    task = get_object_or_404(Task, slug=slug)

    if task.completed_at is None:
        task.completed_at = timezone.now()
    else:
        task.completed_at = None

    task.save()
    return redirect("tasks")


@login_required
def delete_task(request, slug):
    task = get_object_or_404(Task, slug=slug)
    task.delete()
    return redirect("tasks")
