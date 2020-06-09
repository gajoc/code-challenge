import aiohttp
import redis
from sanic import Sanic

from challenge.movies import movies

from backend.challenge.constants import DEFAULT_REDIS_EXPIRE, DEFAULT_REDIS_PORT, DEFAULT_REDIS_HOST, \
    DEFAULT_APP_VARIABLE_PREFIX
from backend.challenge.ghibli import GhibliRepository


def create_app(**kwargs):
    app = Sanic(__name__, load_env=DEFAULT_APP_VARIABLE_PREFIX, **kwargs)
    app.blueprint(movies)

    @app.listener('before_server_start')
    def init(app, loop):
        app.aiohttp_session = aiohttp.ClientSession(loop=loop)
        host = app.config.get('REDIS_HOST', DEFAULT_REDIS_HOST)
        port = app.config.get('REDIS_PORT', DEFAULT_REDIS_PORT)
        app.redis = redis.Redis(host=host, port=port)
        expire_sec = app.config.get('REDIS_EXPIRE', DEFAULT_REDIS_EXPIRE)
        app.repository = GhibliRepository(cache=app.redis, expire_sec=expire_sec)

    @app.listener('after_server_stop')
    def finish(app, loop):
        loop.run_until_complete(app.aiohttp_session.close())
        loop.close()

    return app
