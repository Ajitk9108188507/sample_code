from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.board,
        name="board"
    ),

    path(
        "complete/<int:task_id>/",
        views.complete,
        name="complete"
    ),
]