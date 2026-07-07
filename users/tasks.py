from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def check_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        is_superuser=False,
        last_login__lt=one_month_ago
    )

    count = inactive_users.count()

    if count > 0:
        inactive_users.update(is_active=False)
        return f"Успешно заблокировано пользователей за неактивность: {count}."

    return "Неактивных пользователей для блокировки не найдено."
