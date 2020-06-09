from sanic.blueprints import Blueprint


movies = Blueprint('movies', '/')


from . import views
