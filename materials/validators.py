import re
from rest_framework.exceptions import ValidationError


def validate_youtube_only(value):
    """
    Проверяет, что если в поле передана ссылка, она ведет исключительно на youtube.com
    """
    if not value:
        return value

    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )

    urls = url_pattern.findall(value)

    for url in urls:
        if "youtube.com" not in url and "youtu.be" not in url:
            raise ValidationError("Разрешены ссылки только на ресурс youtube.com.")

    return value
