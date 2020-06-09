from challenge.app import create_app

from backend.challenge.constants import DEFAULT_BACKEND_HOST, DEFAULT_BACKEND_PORT

if __name__ == '__main__':
    app = create_app()
    host = app.config.get('BACKEND_HOST', DEFAULT_BACKEND_HOST)
    port = int(app.config.get('BACKEND_PORT', DEFAULT_BACKEND_PORT))
    app.run(host=host, port=port)
