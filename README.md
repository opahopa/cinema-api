### Cinema api sample
Simplified cinema API which shows the information about movies and comments.

### urls


**movies**
* `/movies/ GET` get the list of movies
* `/movies/ POST` create movie
* `/movies/<id>/ GET` get movie details
* `/movies/<id>/ PUT` update movie
* `/movies/<id>/ PATCH` edit movie
* `/movies/<id>/ DELETE` delete movie

**comments**
* `/movies/<id>/comments/ GET` get the list of movie comments
* `/movies/<id>/comments/ POST` create comment
* `/movies/<id>/comments/<id>/ GET` get comment details
* `/movies/<id>/comments/<id>/ PUT` update comment
* `/movies/<id>/comments/<id>/ PATCH` edit comment
* `/movies/<id>/comments/<id>/ DELETE` delete comment

### installation
1. `viertualenv -v python3 venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python manage.py makemigrations`
5. `python manage.py migrate`

### run app
`python manage.py runserver`

### run tests
`python manage.py test`
