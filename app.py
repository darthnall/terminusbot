import json
import os

import dotenv
from flask import Flask, render_template, request

from auth import Session, Searcher, Validator
from client import Unit, User, Flags
from wialon import Wialon, WialonError


def create_app(token: str, debug_mode_enabled: bool = False):
    app = Flask(__name__)

    if debug_mode_enabled:
        @app.route("/debug", methods=["GET", "POST"])
        def debug():
            if request.method == "GET":
                with Session(token=token) as session:
                    flags = Flags(session=session)
                    data = flags.convert(flags.UNIT_DEFAULT)
                return render_template("debug.html", data=data, title="Debug")
            elif request.method == "POST":
                ...
            else:
                ...

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
