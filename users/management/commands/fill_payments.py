from django.core.management.base import BaseCommand
from users.models import User, Payment
from materials.models import Course, Lesson

class Command(BaseCommand):
    help = 'Заполнение базы данных демонстрационными платежами'

    def handle(self, *args, **options):
        Payment.objects.all().delete()

        user, _ = User.objects.get_or_create(email='test_student@example.com')
        if _ or not user.has_usable_password():
            user.set_password('testpassword123')
            user.save()

        course, _ = Course.objects.get_or_create(title='Python-разработчик', description='Курс по Django')
        lesson, _ = Lesson.objects.get_or_create(title='Введение в ORM', course=course, description='Урок про модели')

        payments_data = [
            {
                "user": user,
                "course": course,
                "amount": 50000.00,
                "payment_method": "transfer"
            },
            {
                "user": user,
                "lesson": lesson,
                "amount": 1500.00,
                "payment_method": "cash"
            }
        ]

        for payment_item in payments_data:
            Payment.objects.create(**payment_item)

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена тестовыми платежами!'))
