from rest_framework import serializers
from .models import Movie, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'created_at', 'movie')
        read_only_fields = ('created_at',)
        extra_kwargs = {'movie': {'write_only': True}}


class MovieListSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'director', 'release_date', 'length', 'comments_count')
        read_only_fields = ('id',)


class MovieDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source='comment')

    class Meta:
        model = Movie
        fields = ('title', 'director', 'description', 'release_date', 'length', 'comments')
