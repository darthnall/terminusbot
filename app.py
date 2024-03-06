import json
import os

import dotenv
from flask import Flask, render_template, request

from auth import Session, Searcher, Validator
from client import Unit, User, Flags
from wialon import Wialon, WialonError


def create_app(token: str, debug_mode_enabled: bool = False):
    app = Flask(__name__)

    @app.route("/register/v/first-name", methods=["POST"])
    def validate_first_name():
        pass

    @app.route("/register/v/last-name", methods=["POST"])
    def validate_last_name():
        pass

    @app.route("/register/v/email", methods=["POST"])
    def validate_email():
        pass

    @app.route("/register/v/asset-name", methods=["POST"])
    def validate_asset_name():
        pass

    @app.route("/register/v/imei", methods=["POST"])
    def validate_imei():
        pass

    @app.route("/register/v/phone-number", methods=["POST"])
    def validate_phone_number():
        pass

    @app.route("/register/v/vin", methods=["POST"])
    def validate_vin():
        pass

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            imei = request.args.get("imei")
            return render_template("register.html", title="Registration", imei=imei)

        elif request.method == "POST":
            data = request.form
            page = "response.html"
            with Session(token=token) as session:
                validator: Validator = Validator(session=session)
                valid, bad_items = validator.validate(data=data)

                user = User(data=data, session=session)
                user.create(name=user.creds["email"], password=user.creds["password"])

                unit = Unit(creds=user.creds, session=session)
                response = unit.assign(user_id=user.creds["userId"])

                if user.email_creds(creds=user.creds):
                    print(f"Credentials emailed to {user.creds['email']}")

                if not isinstance(response, dict):
                    page = "response.raw.html"

                return render_template(
                    page, response=response, title="Response", redirect="register"
                )

    return app


if __name__ == "__main__":
    dotenv.load_dotenv()
    token = os.environ["WIALON_HOSTING_API_TOKEN_DEV"]
    app = create_app(token=token, debug_mode_enabled=True)
    app.run(debug=True)
