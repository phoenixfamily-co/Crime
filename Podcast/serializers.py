from rest_framework import serializers
from .models import PodcastPost


class PodcastPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastPost
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "image",
            "sound",
            "meta_title",
            "meta_description",
            "meta_keywords",
        ]
