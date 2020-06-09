import aiohttp
import redis
from sanic import Sanic

from challenge.movies import movies


def create_app(**kwargs):
    app = Sanic(__name__, load_env='CHALLENGE_', **kwargs)
    app.blueprint(movies)

    @app.listener('before_server_start')
    def init(app, loop):
        app.aiohttp_session = aiohttp.ClientSession(loop=loop)
        host = app.config.get('REDIS_HOST', 'localhost')
        port = app.config.get('REDIS_PORT', 6379)
        app.redis = redis.Redis(host=host, port=port)

    @app.listener('after_server_stop')
    def finish(app, loop):
        loop.run_until_complete(app.aiohttp_session.close())
        loop.close()

    return app