import json
import os

import dotenv
from flask import Flask, render_template, request

from auth import Session
from client import Unit, User
from wialon import Wialon, WialonError


def create_app(token: str | None):
    app = Flask(__name__)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            imei = request.args.get("imei")
            return render_template("register.html", title="Registration", imei=imei)

        elif request.method == "POST":
            data = request.form
            page = "response.html"
            with Session(token=token) as session:
                user = User(data=data, session=session)
                user.create()

                unit = Unit(data=data, session=session)
                response = unit.assign(user_id=user.id)

                if vin := data["vin"] is not None:
                    unit.set_vin(vin)

            if isinstance(response, ImmutableMultiDict):
                page = "response.raw.html"

            return render_template(
                page, response=response, title="Response", redirect="register"
            )

    return app


if __name__ == "__main__":
    dotenv.load_dotenv()
    token = os.environ["WIALON_HOSTING_API_TOKEN_DEV"]
    app = create_app(token=token)
    app.run(debug=True)
