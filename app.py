from auth import Session, Validator
from client import Unit, User
from client.form import create_registration_form, Field
from client.emailuser import EmailUser

from flask import Flask, render_template, request
from flask import session as flask_session

import dotenv
import os
import asyncio
from uuid import UUID, uuid4


def create_app(token: str, secret_key: UUID):
    app = Flask(__name__)
    app.secret_key = str(secret_key)
    app.config['SESSION_TYPE'] = 'filesystem'

    @app.route("/", methods=["GET", "POST"])
    def register():
        if request.method == "GET":

            form = create_registration_form()
            flask_session['REGISTRATION_FORM'] = form

            form["imeiNumber"].user_input = request.args.get("imei")

            return render_template("register.html", title="Registration", form=form, success=None)

        elif request.method == "POST":
            form = flask_session['REGISTRATION_FORM']
            data = request.form
            success = False
            title = "Failure"

            bad_items = Validator(token=token).validate_all(data=data)

            if not bad_items:
                success = True
                title = "Success"

            if "vinNumber" or "phoneNumber" in bad_items:
                success = True
                title = "Success"

            if success:
                with Session(token=token) as session:
                    user = User(data=data, session=session)
                    user.create(name=user.creds["email"], password=user.creds["password"])

                    unit = Unit(creds=user.creds, session=session)
                    unit.assign(user_id=user.creds["userId"])

                    if user.email_creds():
                        print("Email sent successfully")

            form = create_registration_form()
            flask_session['REGISTRATION_FORM'] = form
            return render_template("register.html", title=title, form=form, success=success, bad_items=bad_items)

        else:
            return "404"

    @app.route("/v/first-name", methods=["POST"])
    def validate_first_name():
        field = flask_session['REGISTRATION_FORM']["firstName"]
        _valid = False
        _input = request.form.get("firstName")

        _valid, _msg = Validator(token=token).validate_name(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(
            field=field,
            data=(
                _valid,
                _msg,
                _input
            )
        )

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/last-name", methods=["POST"])
    def validate_last_name():
        field = flask_session['REGISTRATION_FORM']["lastName"]
        _valid = False
        _input = request.form.get("lastName")

        _valid, _msg = Validator(token=token).validate_name(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(
            field=field,
            data=(
                _valid,
                _msg,
                _input
            )
        )

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/email", methods=["POST"])
    def validate_email():
        field = flask_session['REGISTRATION_FORM']["email"]
        _valid = False
        _input = request.form.get("email")

        _valid, _msg = Validator(token=token).validate_email(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(
            field=field,
            data=(
                _valid,
                _msg,
                _input
            )
        )

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/asset-name", methods=["POST"])
    def validate_asset_name():
        field = flask_session['REGISTRATION_FORM']["assetName"]
        _valid = False
        _input = request.form.get("assetName")

        _valid, _msg = Validator(token=token).validate_asset_name(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(
            field=field,
            data=(
                _valid,
                _msg,
                _input
            )
        )

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/phone-number", methods=["POST"])
    def validate_phone_number():
        field = flask_session['REGISTRATION_FORM']["phoneNumber"]
        _valid = False
        _input = request.form.get("phoneNumber")

        _valid, _msg = Validator(token=token).validate_phone_number(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(
            field=field,
            data=(
                _valid,
                _msg,
                _input
            )
        )

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/imei-number", methods=["POST"])
    def validate_imei():
        field = flask_session['REGISTRATION_FORM']["imeiNumber"]
        _valid = False
        _input = request.form.get("imeiNumber")

        _valid, _msg = Validator(token=token).validate_imei_number(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(
            field=field,
            data=(
                _valid,
                _msg,
                _input
            )
        )

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/vin-number", methods=["POST"])
    def validate_vin():
        field = flask_session['REGISTRATION_FORM']["vinNumber"]
        validator = Validator(token=token)

        _valid = False
        _input = request.form.get("vinNumber")

        _valid, _msg = asyncio.run(validator.validate_vin_number(target=_input))

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(
            field=field,
            data=(
                _valid,
                _msg,
                _input
            )
        )

        return render_template("partials/field.html", title="Register", field=field)


    return app


def update_field(field: dict, data: tuple[bool, str, str | None]) -> None:
    field["is_valid"] = data[0]
    field["validation_msg"] = data[1]
    field["user_input"] = data[2]

if __name__ == "__main__":
    dotenv.load_dotenv()
    token = os.environ["WIALON_HOSTING_API_TOKEN_DEV"]
    app = create_app(token=token, secret_key=uuid4())
    app.run(debug=True)
