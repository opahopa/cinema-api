from datetime import datetime, timedelta
from django.test import TestCase
from django.db.utils import IntegrityError
from ..models import Movie


class MovieModelTestCase(TestCase):

    def setUp(self):
        Movie.objects.all().delete()
        self.movie = Movie(title='movie0 word',
                           description='great movie',
                           director='Mr. Black',
                           release_date=datetime.now() - timedelta(days=7),
                           length=7200)
        self.movie.save()

    def test_create_a_movie(self):
        self.assertEqual(1, Movie.objects.count())

    def test_update_a_movie(self):
        self.movie.title = 'another title'
        self.movie.director = 'Mr. Lolo'
        self.movie.length = 3600
        self.movie.description = 'magnificent movie'
        self.movie.save()

        updated = Movie.objects.get(title=self.movie.title)

        self.assertEqual(self.movie.title, updated.title)
        self.assertEqual(self.movie.director, updated.director)
        self.assertEqual(self.movie.length, updated.length)
        self.assertEqual(self.movie.description, updated.description)

    def test_unique_title(self):
        self.movie = Movie(title='movie0 word',
                           description='great movie',
                           director='Mr. Black',
                           release_date=datetime.now() - timedelta(days=7),
                           length=7200)

        self.assertRaises(IntegrityError, self.movie.save)

    def test_delete_a_movie(self):
        self.movie.delete()

        self.assertEqual(0, Movie.objects.count())
