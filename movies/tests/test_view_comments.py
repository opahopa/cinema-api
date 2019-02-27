from datetime import datetime, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Movie, Comment
from ..serializers import CommentSerializer


class MovieViewTestCase(APITestCase):

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
        self.comment_data = {'text': 'this movie was incredibly interesting', 'movie': 1}
        self.response = self.client.post(reverse('comment-list', kwargs={'parent_lookup_movie': 1}),
                                         self.comment_data,
                                         format="json")

    def test_create_comment(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response.data['text'], self.comment_data['text'])

    def test_get_comment(self):
        comment = Comment.objects.get(pk=1)

        response = self.client.get(reverse('comment-list', kwargs={'parent_lookup_movie': 1}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.response.data['text'], comment.text)

    def test_update_comment(self):
        comment = Comment.objects.get(pk=1)
        comment.text = 'new text'

        serializer = CommentSerializer(comment)

        response = self.client.put(reverse('comment-detail', kwargs={'parent_lookup_movie': 1, 'pk': 1}),
                                   {**serializer.data, **{'movie': 1}},
                                   format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], comment.text)

    def test_edit_comment(self):
        text = 'new text'

        response = self.client.patch(reverse('comment-detail', kwargs={'parent_lookup_movie': 1, 'pk': 1}),
                                     {'text': text},
                                     format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], text)

    def test_delete_comment(self):
        response = self.client.delete(reverse('comment-detail', kwargs={'parent_lookup_movie': 1, 'pk': 1}),
                                      format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
