
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields

from models import db, Trail, NationalPark

blp = Blueprint(
    "Trails",
    "trails",
    url_prefix="/api/trail",
    description="Operations on trails",
)


class TrailSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    distance = fields.Float(required=True)
    elevation = fields.Int(required=True)
    difficulty = fields.Str(required=True)
    national_park_id = fields.Int(required=True)


@blp.route("/")
class TrailList(MethodView):

    # Get all trails
    @blp.response(200, TrailSchema(many=True))
    def get(self):
        return Trail.query.order_by(Trail.id).all()

    # Create a trail
    @blp.arguments(TrailSchema)
    @blp.response(201, TrailSchema)
    def post(self, data):
        park = db.session.get(NationalPark, data["national_park_id"])
        if park is None:
            abort(400, message="National park not found")

        trail = Trail(**data)
        db.session.add(trail)
        db.session.commit()
        return trail


@blp.route("/<int:trail_id>")
class TrailDetail(MethodView):

    # Get one trail
    @blp.response(200, TrailSchema)
    def get(self, trail_id):
        trail = db.session.get(Trail, trail_id)
        if trail is None:
            abort(404, message="Trail not found")
        return trail

    # Update a trail
    @blp.arguments(TrailSchema)
    @blp.response(200, TrailSchema)
    def put(self, data, trail_id):
        trail = db.session.get(Trail, trail_id)
        if trail is None:
            abort(404, message="Trail not found")

        park = db.session.get(NationalPark, data["national_park_id"])
        if park is None:
            abort(400, message="National park not found")

        trail.name = data["name"]
        trail.distance = data["distance"]
        trail.elevation = data["elevation"]
        trail.difficulty = data["difficulty"]
        trail.national_park_id = data["national_park_id"]

        db.session.commit()
        return trail

    # Delete a trail
    @blp.response(204)
    def delete(self, trail_id):
        trail = db.session.get(Trail, trail_id)
        if trail is None:
            abort(404, message="Trail not found")

        db.session.delete(trail)
        db.session.commit()
