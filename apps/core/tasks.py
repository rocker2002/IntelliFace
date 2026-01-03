# Temporarily disabled for deployment
# from celery import shared_task
from django.utils import timezone

from .utils import capture_snapshot
from ..users.models import Lecture

# @shared_task
def capture_snapshots_for_active_lectures():
    """
    Placeholder function - Celery tasks temporarily disabled for deployment
    TODO: Re-enable after successful deployment
    """
    print("[INFO] Celery tasks temporarily disabled for deployment")
    return {"message": "Celery tasks temporarily disabled for deployment"}