from . import create_app

app = create_app()

if __name__ == "__main__":
    # Use default Flask dev server for simplicity; in production use gunicorn/uwsgi
    app.run(host="0.0.0.0", port=5001, debug=False)
