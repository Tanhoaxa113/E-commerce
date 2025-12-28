from celery import shared_task
from .models import ProductVideo
import time

@shared_task
def convert_video_hls(video_id):
    try:
        video = ProductVideo.objects.get(id=video_id)

        print(f"--- [CELERY] Đang xử lý video ID: {video_id} ---")
        video.status = 'PROCESSING'
        video.save()

        time.sleep(10)

        video.status = 'DONE'
        video.save()
        print(f"--- [CELERY] Xong video ID: {video_id} ---")
        
    except ProductVideo.DoesNotExist:
        print(f"--- [CELERY] Lỗi: Không tìm thấy video {video_id} ---")