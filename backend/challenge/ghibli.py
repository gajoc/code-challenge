import json
from collections import defaultdict
from typing import Dict, List

from backend.challenge.constants import GHIBLI_FILMS_URL, GHIBLI_PEOPLE_URL


class GhibliRepository:

    def __init__(self, cache, expire_sec: int):
        self._cache = cache
        self._cache_expire = expire_sec

    async def get_movies(self, session) -> List:
        """
        Get movies with acting people from ghibli api or from cache if already available.

        :param session: session object for ghibli api.
        :return: movies.
        """
        movies = self._from_cache("movies")
        if not movies:
            films = await self._from_ghibli(GHIBLI_FILMS_URL, session)
            people = await self._from_ghibli(GHIBLI_PEOPLE_URL, session)
            people_by_film = self._people_by_film(people)
            movies = self._match(films, people_by_film)

            self._to_cache("movies", movies)
        return movies

    @staticmethod
    async def _from_ghibli(url: str, session) -> List:
        """
        Get data from ghibli.

        :param url: resource url on ghibli.
        :param session: ghibli api session object.
        :return: ghibli data list.
        """
        async with session.get(url) as resp:
            data = await resp.json()
            return data

    def _from_cache(self, key: str) -> List:
        """
        Get data from cache (if set) by `key`.

        :param key: data key in cache.
        :return: list of data.
        """
        if self._cache:
            redis_data = self._cache.get(key)
            if redis_data:
                return json.loads(redis_data)
        return []

    def _to_cache(self, key: str, value: Dict) -> None:
        """
        Store `value` in cache under a `key`.

        :param key: cache key.
        :param value: data to store.
        """
        self._cache.setex(key, self._cache_expire, json.dumps(value))

    @staticmethod
    def _people_by_film(people: List) -> Dict:
        """
        Transform collection of people (having aggregated films they acted in) into dict of film
        ids with collection of people.

        :param people: collection of people to be transformed.
        :return: dict of film ids with people acting in this films.
        """
        movies = defaultdict(list)
        for person in people:
            for film in person["films"]:
                film_id = film.split("/")[-1]
                movies[film_id].append(person)
        return movies

    @staticmethod
    def _match(movies: List, people: Dict) -> List:
        """
        Combine `people` with `movies` collection.

        :param movies: collection of movies where appropriate people need to be attached.
        :param people: dict to search for people by film id.
        :return: movies with related people.
        """
        for movie in movies:
            movie["people"] = people.get(movie["id"], [])
        return movies
