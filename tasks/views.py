from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import TaskForm
from .models import Task
from .services import (
    complete_task,
    create_task,
    unlock_expired_tasks,
)


def board(request):

    unlock_expired_tasks()

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():
            create_task(form)

            messages.success(
                request,
                "Task added successfully."
            )

            return redirect("board")

    else:
        form = TaskForm()

    tasks = Task.objects.all().order_by("-created_at")

    return render(
        request,
        "tasks/board.html",
        {
            "form": form,
            "tasks": tasks,
        }
    )


def complete(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    success, hint = complete_task(task)

    if success:

        messages.success(
            request,
            f'"{task.title}" completed!'
        )

    else:

        messages.error(
            request,
            hint
        )

    return redirect("board")