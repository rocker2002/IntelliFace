from celery import shared_task
from django.utils import timezone

from .utils import capture_snapshot
from ..users.models import Lecture

@shared_task
def capture_snapshots_for_active_lectures():
    """
    Celery task to capture snapshots for active lectures
    Note: ML processing is still disabled, this just captures images
    """
    active_lectures = Lecture.objects.filter(end_time__isnull=True)
    results = []
    for lecture in active_lectures:
        for camera in lecture.class_ref.cameras.all():
            try:
                result = capture_snapshot(camera, lecture)
                results.append(f"Captured snapshot for lecture {lecture.id}, camera {camera.id}")
            except Exception as e:
                results.append(f"Error capturing snapshot: {str(e)}")
    
    return {
        "message": "Snapshot capture task completed",
        "results": results,
        "processed_lectures": len(active_lectures)
    }