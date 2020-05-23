from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from master import socketio
from master.models import bookings, cars
from master.car_operation import user_unlock_car, user_return_car
from master.sockets.utils import success_response, error_response

debug = True


@socketio.on("unlock_car")
def unlock_car(data):
<<<<<<< HEAD
    car_number = data["car_number"]
    try:
        result = cars.CarModel.query.filter_by(
            car_number=car_number, lock_status=True).first()
        if result is False:
            return 401, 'this car status is not locking.'
        else:
            return 100, 'this car unlock successfully'
=======
    #    booking_number = data['booking_number']
    car_number = data['car_number']
    try:
        result = cars.CarModel.query.filter_by(
            car_number=car_number, lock_status=True).first()
        if result is None:
            return 401, 'the car is unlock.'
        else:
            return 100, result
>>>>>>> 488b412b9c8e2fd2ed0de57500f9be0d27385238
    except Exception as e:
        error = str(e.__dict__['orig'])
        return 500, error


@socketio.on("return_car")
def return_car(data):
<<<<<<< HEAD
    #car_number = data["car_number"]
    try:
        result = True
        if result is False:
            return 'this car status is not renting.'
        else:
            return 'this car return successfully'
    except Exception as e:
        error = str(e.__dict__['orig'])
        return error
=======
    if debug:
        return success_response(
            username=username, access_token="access_token", refresh_token="refresh_token",
        )
    ok, res = user_return_car(username)
    return success_response(
        return_car_result=ok, return_car_response=res
    )
>>>>>>> 488b412b9c8e2fd2ed0de57500f9be0d27385238
