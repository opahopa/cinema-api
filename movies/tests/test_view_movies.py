import asyncio

from datetime import datetime, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Movie
from ..serializers import MovieSerializer


class MovieViewTestCase(APITestCase):

    def setUp(self):
        Movie.objects.all().delete()
        self.movie_data = {'title': 'movie0 word',
                           'description': 'great movie0',
                           'director': 'Mr. Black',
                           'release_date': (datetime.now() - timedelta(days=7)).date(),
                           'length': 7200}
        self.response = self.client.post(reverse('movie-list'), self.movie_data, format="json")

    def test_create_movie(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response.data['title'], self.movie_data['title'])

    def test_create_invalid_movie(self):
        """ this can be expended to test each param """

        movie_data = {'title': ('s' for i in range(0, 300)),
                      'description': 'great movie0',
                      'director': 'Mr. Black',
                      'release_date': '2340-01-2388888',
                      'length': 7200}
        response = self.client.post(reverse('movie-list'), movie_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_movies(self):
        response = self.client.get(reverse('movie-list'), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(self.response.data) > 0)

    def test_get_movie(self):
        movie = Movie.objects.get(pk=1)

        response = self.client.get(reverse('movie-detail', kwargs={'pk': 1}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.response.data['title'], movie.title)

    def test_show_comments_count(self):
        response = self.client.get(reverse('movie-detail', kwargs={'pk': 1}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comments_count'], 0)

    def test_filter_orderby_release_date_desc(self):
        self.async_run(self.add_more_movies)
        response = self.client.get('%s?ordering=%s' % (reverse('movie-list'), '-release_date'), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "movie1 word")

    def test_filter_orderby_release_date_asc(self):
        self.async_run(self.add_more_movies)
        response = self.client.get('%s?ordering=%s' % (reverse('movie-list'), 'release_date'), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "movie2 word")

    def test_filter_orderby_comments_count_desc(self):
        self.async_run(self.add_more_movies)

        self.client.post(reverse('comment-list', kwargs={'parent_lookup_movie': 1}),
                         {'text': 'this movie was incredibly interesting', 'movie': 1},
                         format="json")

        response = self.client.get('%s?ordering=%s' % (reverse('movie-list'), '-comments_count'), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 1)

    def test_filter_orderby_comments_count_asc(self):
        self.async_run(self.add_more_movies)

        self.client.post(reverse('comment-list', kwargs={'parent_lookup_movie': 1}),
                         {'text': 'this movie was incredibly interesting', 'movie': 1},
                         format="json")

        response = self.client.get('%s?ordering=%s' % (reverse('movie-list'), 'comments_count'), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data[0]['id'], 1)

    def test_update_movie(self):
        movie = Movie.objects.get(pk=1)
        movie.description = 'new description'

        serializer = MovieSerializer(movie)

        response = self.client.put(reverse('movie-detail', kwargs={'pk': 1}), serializer.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], movie.description)

    def test_edit_movie(self):
        description = 'new description'
        response = self.client.patch(reverse('movie-detail', kwargs={'pk': 1}),
                                     {'description': description},
                                     format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], description)

    def test_delete_movie(self):
        response = self.client.delete(reverse('movie-detail', kwargs={'pk': 1}), format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    async def add_more_movies(self):
        movies = [
            {
                'title': 'movie1 word',
                'description': 'great movie1',
                'director': 'Mr. Black',
                'release_date': (datetime.now() - timedelta(days=5)).date(),
                'length': 7200
            },
            {
                'title': 'movie2 word',
                'description': 'great movie2',
                'director': 'Mr. Black',
                'release_date': (datetime.now() - timedelta(days=10)).date(),
                'length': 7200
            },
            {
                'title': 'movie3 word',
                'description': 'great movie3',
                'director': 'Mr. Black',
                'release_date': (datetime.now() - timedelta(days=8)).date(),
                'length': 7200
            },
        ]

        return await asyncio.gather(*(self.movies_post(m) for m in movies))

    async def movies_post(self, data):
        return self.client.post(reverse('movie-list'), data, format="json")

    def async_run(self, f):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f())
