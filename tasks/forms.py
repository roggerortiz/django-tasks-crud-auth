from django.forms import (
    Form,
    CharField,
    EmailField,
    TextInput,
    Textarea,
    CheckboxInput,
    PasswordInput,
)


class SignUpForm(Form):
    first_name = CharField(
        required=True,
        max_length=150,
        label="First Name",
        widget=TextInput(attrs={"class": "form-control"}),
    )
    last_name = CharField(
        required=True,
        max_length=150,
        label="Last Name",
        widget=TextInput(attrs={"class": "form-control"}),
    )
    email = EmailField(
        required=True,
        max_length=254,
        label="Email",
        widget=TextInput(attrs={"class": "form-control"}),
    )
    username = CharField(
        required=True,
        max_length=150,
        label="Username",
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        widget=TextInput(attrs={"class": "form-control"}),
    )
    password1 = CharField(
        required=True,
        max_length=150,
        label="Password",
        widget=PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = CharField(
        required=True,
        max_length=150,
        label="Password confirmation",
        help_text="Enter the same password as before, for verification.",
        widget=PasswordInput(attrs={"class": "form-control"}),
    )


class SignInForm(Form):
    username = CharField(
        required=True,
        max_length=150,
        label="Username",
        widget=TextInput(attrs={"class": "form-control"}),
    )
    password = CharField(
        required=True,
        max_length=150,
        label="Password",
        widget=PasswordInput(attrs={"class": "form-control"}),
    )


class TaskForm(Form):
    title = CharField(
        required=True,
        max_length=100,
        label="Title",
        widget=TextInput(attrs={"class": "form-control"}),
    )
    description = CharField(
        required=False,
        label="Description",
        widget=Textarea(attrs={"class": "form-control resize-none"}),
    )
    important = CharField(
        required=False,
        label="Important",
        widget=CheckboxInput(attrs={"class": "form-check-input"}),
    )
