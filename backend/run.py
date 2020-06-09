from challenge.app import create_app


if __name__ == '__main__':
    app = create_app()
    host = app.config.get('BACKEND_HOST', 'localhost')
    port = int(app.config.get('BACKEND_PORT', 5000))
    app.run(host=host, port=port)
