from sanic import response, views

from . import movies as bp


class MoviesView(views.HTTPMethodView):

    async def get(self, request):
        return response.json({"challenge accepted": True}, status=200)


bp.add_route(MoviesView.as_view(), '/movies')
