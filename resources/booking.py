from flask_restful import Resource

from managers.auth import auth


class Booking(Resource):
    @auth.login_required
    def get(self, booking_id):
        user = auth.current_user()


