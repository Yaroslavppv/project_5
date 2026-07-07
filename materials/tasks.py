from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from materials.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return f"Курс с ID {course_id} не найден."

    now = timezone.now()
    if course.updated_at and (now - course.updated_at) < timedelta(hours=4):
        return f"Рассылка отменена. С момента последнего обновления курса '{course.title}' прошло меньше 4 часов."

    subscriptions = Subscription.objects.filter(course=course)
    recipient_list = [sub.user.email for sub in subscriptions if sub.user.email]

    if not recipient_list:
        return f"У курса '{course.title}' нет активных подписчиков."

    subject = f"Обновление материалов курса: {course.title}"
    message = f"Здравствуйте!\n\nМатериалы курса '{course.title}' были изменены. Загляните на платформу!"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    return f"Успешно отправлено {len(recipient_list)} писем."
