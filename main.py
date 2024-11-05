from decouple import config

from config import create_app
from db import db


environment = config("CONFIG_ENV")
app = create_app(environment)


@app.teardown_appcontext
def close_request(response):
    db.session.commit()
    return response
