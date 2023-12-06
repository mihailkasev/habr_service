import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from hubs.models import Hub


@receiver(post_save, sender=Hub)
def add_or_update_task(sender, instance: Hub, created: bool, **kwargs):
    """Добавляет или обновляет периодическую задачу на основе периода парсинга хаба"""
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=instance.parse_period,
        period=IntervalSchedule.MINUTES,
    )
    if created:
        PeriodicTask.objects.create(
            interval=schedule,
            name=instance.link,
            task='tasks.tasks.request_hub',
            args=json.dumps([instance.link]),
        )
    else:
        PeriodicTask.objects.update(
            interval=schedule
        )
