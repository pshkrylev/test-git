import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from news.management.commands.send_weekly_newsletter import Command as WeeklyNewsletterCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Запускает планировщик задач"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Запускаем еженедельную рассылку каждую пятницу в 10:00
        scheduler.add_job(
            WeeklyNewsletterCommand().handle,
            trigger=CronTrigger(day_of_week='fri', hour=10, minute=0),
            id="weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Добавлена задача еженедельной рассылки")

        try:
            logger.info("Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик остановлен")