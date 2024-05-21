import requests

from auth import Validator
from client.form import create_registration_form

from datetime import datetime

from webhooks.notifier import PhoneNotifier
from webhooks.phonemessage import create_message

from flask import Flask, session, render_template, request, jsonify

from config import Config


def create_app():
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SECRET_KEY=Config.SECRET_KEY,
    )
    app.config.from_object(__name__)

    @app.route("/", methods=["GET", "POST"])
    def register():
        form = create_registration_form()
        if request.method == "GET":
            return render_template(
                "register.html",
                title="Register",
                success=None,
                form=form,
            )

        if request.method == "POST":
            params = {
                "email": request.values.get("email"),
                "imei": request.values.get("imeiNumber"),
                "asset_name": request.values.get("assetName"),
            }
            requests.post(
                "https://api.terminusgps.com/v1/forms/create_wialon_user", params=params
            )

            return render_template(
                "register.html",
                title="Register",
                success=True,
                form=form,
            )

    @app.route("/v/first-name", methods=["POST"])
    def validate_first_name():
        field = session["REGISTRATION_FORM"]["firstName"]
        _valid = False
        _input = request.form.get("firstName")

        _valid, _msg = Validator().validate_first_name(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/last-name", methods=["POST"])
    def validate_last_name():
        field = session["REGISTRATION_FORM"]["lastName"]
        _valid = False
        _input = request.form.get("lastName")

        _valid, _msg = Validator().validate_last_name(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/email", methods=["POST"])
    def validate_email():
        field = session["REGISTRATION_FORM"]["email"]
        _valid = False
        _input = request.form.get("email")

        _valid, _msg = Validator().validate_email(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/asset-name", methods=["POST"])
    def validate_asset_name():
        field = session["REGISTRATION_FORM"]["assetName"]
        _valid = False
        _input = request.form.get("assetName")

        _valid, _msg = Validator().validate_asset_name(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/phone-number", methods=["POST"])
    def validate_phone_number():
        field = session["REGISTRATION_FORM"]["phoneNumber"]
        _valid = False
        _input = request.form.get("phoneNumber")

        _valid, _msg = Validator().validate_phone_number(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/imei-number", methods=["POST"])
    def validate_imei():
        field = session["REGISTRATION_FORM"]["imeiNumber"]

        _valid = False
        _input = request.form.get("imeiNumber")

        _valid, _msg = Validator().validate_imei_number(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/vin-number", methods=["POST"])
    def validate_vin():
        field = session["REGISTRATION_FORM"]["vinNumber"]

        _valid = False
        _input = request.form.get("vinNumber")

        _valid, _msg = Validator().validate_vin_number(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    return app


def update_field(field: dict, data: tuple[bool, str, str | None]) -> None:
    field["is_valid"] = data[0]
    field["validation_msg"] = data[1]
    field["user_input"] = data[2]


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
