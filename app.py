
from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api

from config import Config
from models import db, NationalPark, Trail, Booking

from routes import blp as national_park_blp
from trail_routes import blp as trail_blp
from booking_routes import blp as booking_blp
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200"])
app.config.from_object(Config)

app.config["API_TITLE"] = "National Park API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = (
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
)

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

api.register_blueprint(national_park_blp)
api.register_blueprint(trail_blp)
api.register_blueprint(booking_blp)


@app.get("/")
def home():
    return {"message": "National Park Python API is running"}


if __name__ == "__main__":
    app.run(debug=True)
