from decouple import config
from flask import render_template

from config import create_app
from db import db


environment = config("CONFIG_ENV")
app = create_app(environment)

@app.route('/')  # Root URL of your app
def home():
    return render_template('booking.html')  # Assumes 'index.html' is in the 'templates' folder

if __name__ == "__main__":
    app.run()


@app.teardown_appcontext
def close_request(response):
    db.session.commit()
    return response
