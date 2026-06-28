from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_only


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_only], required=False, allow_null=True)

    description = serializers.CharField(validators=[validate_youtube_only], required=False, allow_null=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    is_subscribed = serializers.SerializerMethodField()

    description = serializers.CharField(validators=[validate_youtube_only], required=False, allow_null=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'is_subscribed', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')

        if not request or not request.user or request.user.is_anonymous:
            return False

        return Subscription.objects.filter(user=request.user, course=obj).exists()

