
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields

from models import db, NationalPark

blp = Blueprint(
    "NationalParks",
    "national_parks",
    url_prefix="/api/nationalpark",
    description="Operations on national parks",
)


class NationalParkSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    state = fields.Str(required=True)
    picture = fields.Str(allow_none=True)
    created = fields.DateTime(allow_none=True)
    established = fields.DateTime(allow_none=True)


@blp.route("/")
class NationalParkList(MethodView):

    @blp.response(200, NationalParkSchema(many=True))
    def get(self):
        return NationalPark.query.order_by(NationalPark.id).all()

    @blp.arguments(NationalParkSchema)
    @blp.response(201, NationalParkSchema)
    def post(self, data):
        park = NationalPark(**data)
        db.session.add(park)
        db.session.commit()
        return park


@blp.route("/<int:park_id>")
class NationalParkDetail(MethodView):

    @blp.response(200, NationalParkSchema)
    def get(self, park_id):
        park = db.session.get(NationalPark, park_id)
        if park is None:
            abort(404, message="National park not found")
        return park

    @blp.arguments(NationalParkSchema)
    @blp.response(200, NationalParkSchema)
    def put(self, data, park_id):
        park = db.session.get(NationalPark, park_id)
        if park is None:
            abort(404, message="National park not found")

        park.name = data["name"]
        park.state = data["state"]
        park.picture = data.get("picture")
        park.created = data.get("created")
        park.established = data.get("established")

        db.session.commit()
        return park

    @blp.response(204)
    def delete(self, park_id):
        park = db.session.get(NationalPark, park_id)
        if park is None:
            abort(404, message="National park not found")

        db.session.delete(park)
        db.session.commit()

