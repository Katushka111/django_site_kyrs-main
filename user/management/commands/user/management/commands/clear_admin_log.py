from datetime import timedelta

from django.contrib.admin.models import LogEntry
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = (
        "Очистка истории действий администратора (django.contrib.admin LogEntry). "
        "По умолчанию удаляет записи старше N дней (90). Используйте --all для полной очистки."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Удалить записи старше указанного количества дней (по умолчанию 90)",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Удалить ВСЕ записи (игнорирует --days)",
        )

    def handle(self, *args, **options):
        delete_all: bool = options["all"]
        days: int = options["days"]

        if delete_all:
            deleted_count, _ = LogEntry.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"Удалено записей: {deleted_count}"))
            return

        if days < 0:
            raise CommandError("Параметр --days должен быть неотрицательным")

        cutoff = timezone.now() - timedelta(days=days)
        qs = LogEntry.objects.filter(action_time__lt=cutoff)
        deleted_count, _ = qs.delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Удалено записей старше {days} дн.: {deleted_count} (до {cutoff.strftime('%Y-%m-%d %H:%M:%S')})"
            )
        )


