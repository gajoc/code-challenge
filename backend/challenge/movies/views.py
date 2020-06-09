from sanic import response, views

from . import movies as bp


class MoviesView(views.HTTPMethodView):

    async def get(self, request):
        data = await request.app.repository.get_movies(session=request.app.aiohttp_session)
        return response.json(data, status=200)


bp.add_route(MoviesView.as_view(), '/movies')
