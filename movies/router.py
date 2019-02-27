from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedSimpleRouter
from .views import MovieViewSet, CommentViewSet


router = DefaultRouter()


router = ExtendedSimpleRouter()
(
    router.register('movies', MovieViewSet, base_name='movie')
          .register('comments',
                    CommentViewSet,
                    base_name='comment',
                    parents_query_lookups=['movie'])
)

