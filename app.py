import json
import os

import dotenv
from flask import Flask, render_template, request

from auth import Session, Searcher, Validator
from client import Unit, User
from wialon import Wialon, WialonError


def create_app(token: str):
    app = Flask(__name__)



    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            imei = request.args.get("imei")
            return render_template("register.html", title="Registration", imei=imei)

        elif request.method == "POST":
            data = request.form
            page = "response.html"
            # Open session > Create the user > Add unit to user > email credentials
            with Session(token=token) as session:
                user = User(data=data, session=session)
                user.create(
                    name = user.creds["email"],
                    password = user.creds["password"]
                )

                unit = Unit(creds=user.creds, session=session)
                response = unit.assign(user_id=user.creds["userId"])


            if user.email_creds():
                print(f"Credentials emailed to {user.creds['email']}")

            if not isinstance(response, dict):
                page = "response.raw.html"

            return render_template(
                page, response=response, title="Response", redirect="register"
            )
        else:
            return "404"

    @app.route("/register/imei", methods=["GET", "POST"])
    def validate_imei():
        if request.method == "GET":
            imei = "869084062042605"
            if Validator(token=token).validate_imei(target=imei):
                print("Found IMEI")
            else:
                print("IMEI not found")

            return render_template("register.html", title="Registration", imei=imei)

        elif request.method == "POST":
            return render_template("index.html", title=None)

        else:
            return render_template("index.html", title=None)

    """
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


    @app.route("/register/v/phone-number", methods=["POST"])
    def validate_phone_number():
        pass

    @app.route("/register/v/vin", methods=["POST"])
    def validate_vin():
        pass
    """


    return app


if __name__ == "__main__":
    dotenv.load_dotenv()
    token = os.environ["WIALON_HOSTING_API_TOKEN_DEV"]
    app = create_app(token=token)
    app.run(debug=True)
