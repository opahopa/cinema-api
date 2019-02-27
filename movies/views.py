from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.db.models import Count
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer


class MovieViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    ordering_fields = ['release_date', 'comments_count']

    def get_queryset(self):
        queryset = Movie.objects.annotate(comments_count=Count('comment')).all()
        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None and ordering.lstrip('-') in self.ordering_fields:
            queryset = queryset.order_by(ordering)

        return queryset


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
