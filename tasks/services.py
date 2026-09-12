from datetime import timedelta

from django.utils import timezone

from .models import Task


def unlock_expired_tasks():
    """
    Unlock tasks whose 5-minute lock has expired.
    """

    now = timezone.now()

    Task.objects.filter(
        status="LOCKED",
        locked_until__lte=now
    ).update(
        status="PENDING",
        locked_until=None
    )


def create_task(form):
    """
    Create a task and apply the
    3-tasks-within-2-minutes rule.
    """

    now = timezone.now()

    recent_tasks = Task.objects.filter(
        created_at__gte=now - timedelta(minutes=2),
        created_at__lte=now
    ).count()

    task = form.save(commit=False)
    task.save()

    # If 3 tasks were already created
    # during the previous 2 minutes,
    # lock the 4th task.
    if recent_tasks >= 3:

        task.status = "LOCKED"

        task.locked_until = (
            now + timedelta(minutes=5)
        )

        task.save(
            update_fields=[
                "status",
                "locked_until"
            ]
        )

    return task


def get_allowed_time(task):
    """
    Determine the actual time allowed for a task.

    Even minute = full estimated time
    Odd minute  = half estimated time
    """

    minute = task.created_at.minute

    if minute % 2 == 0:
        return task.estimated_time

    return max(1, task.estimated_time // 2)


def is_task_expired(task):
    allowed_minutes = get_allowed_time(task)

    deadline = (
        task.created_at
        + timedelta(minutes=allowed_minutes)
    )

    return timezone.now() > deadline



def has_unfinished_low_tasks():
    return Task.objects.filter(
        priority="LOW"
    ).exclude(
        status="COMPLETED"
    ).exists()


def hidden_completion_check(task):
    """
    Internal rule.

    The user should never be shown
    this calculation.
    """

    value = (
        len(task.title)
        + task.estimated_time
        + task.created_at.minute
    )

    return value % 7 != 0



def complete_task(task):

    unlock_expired_tasks()

    # Rule 1: High priority dependency
    if task.priority == "HIGH":

        if has_unfinished_low_tasks():

            return False, (
                "A smaller stone still remains on the road."
            )

    # Rule 2: Locked task
    if task.status == "LOCKED":

        return False, (
            "The door opens when the fifth shadow fades."
        )

    # Don't allow completion twice
    if task.status == "COMPLETED":

        return False, (
            "What is already finished cannot be finished again."
        )

    # Rule 3: Time limit
    if is_task_expired(task):

        task.status = "EXPIRED"
        task.save(update_fields=["status"])

        return False, (
            "The clock has already chosen another path."
        )

    # Rule 4: Hidden logic
    if not hidden_completion_check(task):

        return False, (
            "The pattern does not recognize this ending."
        )

    # Everything passed
    task.status = "COMPLETED"
    task.save(update_fields=["status"])

    return True, None