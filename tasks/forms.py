from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            "title",
            "priority",
            "estimated_time",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter task title"
                }
            ),

            "estimated_time": forms.NumberInput(
                attrs={
                    "min": 1,
                    "placeholder": "Minutes"
                }
            ),
        }