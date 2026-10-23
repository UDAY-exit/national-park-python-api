
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class NationalPark(db.Model):
    __tablename__ = "NationalParks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(500), nullable=True)
    created = db.Column(db.DateTime, nullable=True)
    established = db.Column(db.DateTime, nullable=True)

    trails = db.relationship(
        "Trail",
        back_populates="national_park",
        cascade="all, delete-orphan"
    )


class Trail(db.Model):
    __tablename__ = "Trails"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)

    national_park_id = db.Column(
        db.Integer,
        db.ForeignKey("NationalParks.id"),
        nullable=False
    )

    national_park = db.relationship(
        "NationalPark",
        back_populates="trails"
    )


class Booking(db.Model):
    __tablename__ = "Bookings"

    id = db.Column(db.Integer, primary_key=True)
    national_park_id = db.Column(
        db.Integer,
        db.ForeignKey("NationalParks.id"),
        nullable=False
    )
    customer_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    adults = db.Column(db.Integer, nullable=False, default=1)
    children = db.Column(db.Integer, nullable=False, default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")

    national_park = db.relationship("NationalPark")
