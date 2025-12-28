import subprocess
import tempfile
from urllib.parse import quote

from django.core.files.base import ContentFile
from django.utils import timezone

from apps.users.models import Snapshot


def capture_snapshot(camera, lecture):
    # import pdb; pdb.set_trace()
    nvr_ip = camera.ip_address
    nvr_username = camera.username
    nvr_password = quote(camera.password, safe="")
    channel = camera.channel_number

    rtsp_url = (
        f"rtsp://{nvr_username}:{nvr_password}@{nvr_ip}:554/"
        f"cam/realmonitor?channel={channel}&subtype=0&unicast=true&proto=Onvif"
    )

    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")

    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_file:
        cmd = [
            "ffmpeg",
            "-rtsp_transport", "tcp",
            "-i", rtsp_url,
            "-frames:v", "1",
            "-q:v", "2",
            tmp_file.name,
            "-y"
        ]

        print("Capturing snapshot using FFmpeg...")

        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if p.returncode != 0:
            print("FFmpeg failed:", p.stderr.decode())
            return

        tmp_file.seek(0)
        image_bytes = tmp_file.read()

        django_file = ContentFile(
            image_bytes,
            name=f"{camera.name}_{timestamp}.jpg"
        )

        snapshot = Snapshot.objects.create(
            lecture=lecture,
            camera=camera,
            image=django_file
        )

        print(f"Snapshot saved →", snapshot.id)
