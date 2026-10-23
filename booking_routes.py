
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields

from models import db, Booking, NationalPark

blp = Blueprint(
    "Bookings",
    "bookings",
    url_prefix="/api/booking",
    description="Operations on bookings",
)


class BookingSchema(Schema):
    id = fields.Int(dump_only=True)
    national_park_id = fields.Int(required=True)
    customer_name = fields.Str(required=True)
    email = fields.Email(required=True)
    booking_date = fields.Date(required=True)
    adults = fields.Int(required=True, validate=lambda value: value >= 1)
    children = fields.Int(required=True, validate=lambda value: value >= 0)
    total_amount = fields.Decimal(
        as_string=True,
        required=True,
        validate=lambda value: value >= 0,
    )
    status = fields.Str(load_default="Pending")


@blp.route("/")
class BookingList(MethodView):

    # Get all bookings
    @blp.response(200, BookingSchema(many=True))
    def get(self):
        return Booking.query.order_by(Booking.id).all()

    # Create a booking
    @blp.arguments(BookingSchema)
    @blp.response(201, BookingSchema)
    def post(self, data):
        park = db.session.get(NationalPark, data["national_park_id"])
        if park is None:
            abort(400, message="National park not found")

        booking = Booking(**data)
        db.session.add(booking)
        db.session.commit()
        return booking


@blp.route("/<int:booking_id>")
class BookingDetail(MethodView):

    # Get one booking
    @blp.response(200, BookingSchema)
    def get(self, booking_id):
        booking = db.session.get(Booking, booking_id)
        if booking is None:
            abort(404, message="Booking not found")
        return booking

    # Update a booking
    @blp.arguments(BookingSchema)
    @blp.response(200, BookingSchema)
    def put(self, data, booking_id):
        booking = db.session.get(Booking, booking_id)
        if booking is None:
            abort(404, message="Booking not found")

        park = db.session.get(NationalPark, data["national_park_id"])
        if park is None:
            abort(400, message="National park not found")

        booking.national_park_id = data["national_park_id"]
        booking.customer_name = data["customer_name"]
        booking.email = data["email"]
        booking.booking_date = data["booking_date"]
        booking.adults = data["adults"]
        booking.children = data["children"]
        booking.total_amount = data["total_amount"]
        booking.status = data["status"]

        db.session.commit()
        return booking

    # Delete a booking
    @blp.response(204)
    def delete(self, booking_id):
        booking = db.session.get(Booking, booking_id)
        if booking is None:
            abort(404, message="Booking not found")

        db.session.delete(booking)
        db.session.commit()
