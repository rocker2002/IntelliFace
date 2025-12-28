from celery import shared_task
from django.utils import timezone

from .utils import capture_snapshot
from ..users.models import Lecture

# @shared_task
def capture_snapshots_for_active_lectures():
    active_lectures = Lecture.objects.filter(end_time__isnull=True)
    for lecture in active_lectures:
        for camera in lecture.class_ref.cameras.all():
            capture_snapshot(camera, lecture)