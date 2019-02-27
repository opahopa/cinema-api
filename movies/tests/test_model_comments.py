from datetime import datetime, timedelta
from django.test import TestCase
from ..models import Comment, Movie


class CommentModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.movie = Movie(title='movie0 word',
                          description='great movie',
                          director='Mr. Black',
                          release_date=datetime.now() - timedelta(days=7),
                          length=7200)

    def setUp(self):
        self.movie.save()
        Comment.objects.all().delete()
        self.comment = Comment(text='this movie was seriously troubled',
                               created_at=datetime.now(),
                               movie=self.movie)
        self.comment.save()

    def test_create_comment(self):
        self.assertEqual(1, Comment.objects.count())

    def test_update_comment(self):
        self.comment.text = 'this movie is incredibly good'
        self.comment.save()

        updated = Comment.objects.get(id=self.comment.id)

        self.assertEqual(self.comment.text, updated.text)

    def test_delete_comment(self):
        self.comment.delete()

        self.assertEqual(0, Comment.objects.count())

    def test_delete_comment_on_movie_deleted(self):
        self.assertEqual(1, Comment.objects.count())
        self.movie.delete()
        self.assertEqual(0, Comment.objects.count())
