from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson, Subscription

# Create your tests here.

User = get_user_model()


class MaterialsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="student@example.com", password="password123")
        self.another_user = User.objects.create_user(email="stranger@example.com", password="password123")

        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание курса",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Описание урока",
            course=self.course,
            owner=self.user
        )

    # ==========================================
    # ТЕСТЫ CRUD УРОКОВ
    # ==========================================

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-create")
        data = {
            "title": "Новый урок",
            "description": "Разрешенное описание",
            "course": self.course.id,
            "video_url": "https://youtube.com"
        }

        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(response.json()["owner"], self.user.id)

    def test_create_lesson_invalid_url(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-create")
        data = {
            "title": "Урок со спамом",
            "course": self.course.id,
            "video_url": "https://github.com"
        }

        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("video_url", response.json())

    def test_get_lessons_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_get_lesson_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-get", kwargs={"pk": self.lesson.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], self.lesson.title)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-update", kwargs={"pk": self.lesson.pk})
        data = {"title": "Обновленное название"}

        response = self.client.patch(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Обновленное название")

    def test_delete_lesson_by_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-delete", kwargs={"pk": self.lesson.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_by_stranger(self):
        self.client.force_authenticate(user=self.another_user)
        url = reverse("materials:lesson-delete", kwargs={"pk": self.lesson.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    # ==========================================
    # ТЕСТЫ ФУНКЦИОНАЛА ПОДПИСКИ
    # ==========================================

    def test_subscription_toggle(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:course-subscribe")
        data = {"course_id": self.course.id}

        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "Подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "Подписка удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())