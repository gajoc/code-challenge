### Things TODO and issues encountered


####1. Unittests are missing and current simple test is broken.

pytest-sanic and aiohttp (for getting data from ghibli api) are using different
event loops. That`s why tests cannot be run properly. Could not find a solution how
to force both libs to use same and only one event loop at the same time.

####2. marshmallow schemas can be added to validate data from ghibli api (to ensure incoming proper data format).

####3. authentication can be added to be service (like jwt).


Points 1. not resolved due to lack of ideas.
Points 2. not resolved due to lack of time.
Points 3. not resolved due to lack of time to refresh knowledge and docs data.
