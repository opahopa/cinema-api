from rest_framework import serializers
from .models import Movie, Comment


class MovieSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'director', 'description', 'release_date', 'comments_count', 'length')
        read_only_fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'created_at', 'movie')
        read_only_fields = ('created_at',)
