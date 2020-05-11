from flask_restful import reqparse, abort, Resource, inputs
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from master import app, api, db
from sqlalchemy.exc import SQLAlchemyError
from master.models import bookings, cars

parser_new = reqparse.RequestParser()
parser_new.add_argument('car_number', type = inputs.regex('^[A-Za-z0-9]{1,6}$'), required=True)

# "2013-01-01T06:00/2013-01-01T12:00" -> datetime(2013, 1, 1, 6), datetime(2013, 1, 1, 12)
# A tuple of depature and return time in iso8601 format
parser_new.add_argument('booking_period', type=inputs.iso8601interval)

parser_cancel = reqparse.RequestParser()
parser_cancel.add_argument('booking_id', type = inputs.positive, required=True)

def check_and_book(car_number):
    try:
        result = cars.CarModel.query.filter_by(car_number=car_number).first()
        if result is None:
            abort(500, message="Car {} doesn't exisit.".format(car_number))
        elif not result.available:
            abort(403, message='The car has already been booked.')
        else:
            result.available=False
            db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return {'message': error}, 500

class MyBookedCars(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        try:
            result = bookings.BookingModel.query.filter_by(
                username=current_user).all()
            booked_cars = list(map(lambda item: {
                'booking_id': item.booking_id,
                'car_number': item.car_number,
                'created_at': item.created_at.isoformat()}, result))
            return booked_cars, 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class NewBooking(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()

        args = parser_new.parse_args()
        car_number = args['car_number']
        car_number = car_number.upper()
        booking_period = args['booking_period']
        departure_time = booking_period[0]
        return_time = booking_period[1]

        check_and_book(car_number)

        new_booking = bookings.BookingModel(
            car_number=car_number,
            username=current_user,
            departure_time = departure_time,
            return_time = return_time
        )

        try:

            new_booking.save_to_db()
            return {
                'message': "Your booking (id: {}) for car {} has been successfully created.".format(new_booking.booking_id, car_number)
            }
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class CancelBooking(Resource):
    @jwt_required
    def put(self):
        args = parser_cancel.parse_args()
        current_booking = args['booking_id']

        try:
            result_booking = bookings.BookingModel.query.filter_by(
                booking_id=current_booking).first()
            result_booking.active = False

            result_car = cars.CarModel.query.filter_by(car_number= result_booking.car_number).first()
            result_car.available = True

            db.session.commit()
            return ({
                'message': "Your booking {} has been canceled.".format(current_booking)
            }, 200)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


api.add_resource(MyBookedCars, '/bookings/me')
api.add_resource(NewBooking, '/bookings/new')
api.add_resource(CancelBooking, '/bookings/cancel')