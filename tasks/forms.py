from django.contrib.auth.models import User
from django import forms


class CreateTask(forms.Form):
    title = forms.CharField(
        required=True,
        max_length=200,
        label="Title",
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}),
    )
    description = forms.CharField(
        required=False,
        label="Description",
        widget=forms.Textarea(
            attrs={"class": "form-control form-control-sm resize-none"}
        ),
    )
    user = forms.ModelChoiceField(
        required=True,
        queryset=User.objects.all(),
        label="User",
        to_field_name="id",
        empty_label="- Select User -",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
