from auth import Session, Validator
from client import Unit, User
from client.form import create_registration_form

from flask import Flask, render_template, request

import dotenv
import os


def create_app(token: str):
    app = Flask(__name__)

    form = create_registration_form()

    @app.route("/", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            form[-1].user_input = request.args.get("imei")

            return render_template("register.html", title="Registration", form=form)

        elif request.method == "POST":
            data = request.form
            bad_data = validate(Validator(token=token), data=data)

            if bad_data:
                success = False

            with Session(token=token) as session:
                user = User(data=data, session=session)
                user.create(name=user.creds["email"], password=user.creds["password"])

                unit = Unit(creds=user.creds, session=session)
                unit.assign(user_id=user.creds["userId"])

                user.email_creds()

            return render_template("register.html", form=form, success=success)

        else:
            return "404"

    @app.route("/v/first-name", methods=["POST"])
    def validate_first_name():
        _valid = False
        _input = request.form.get("firstName")

        if Validator(token=token).validate_name(target=_input):
            _valid = True

        form[0].validation_result = _valid
        form[0].user_input = _input

        return render_template("partials/field.html", title="Register", field=form[0])

    @app.route("/v/last-name", methods=["POST"])
    def validate_last_name():
        _valid = False
        _input = request.form.get("lastName")

        if Validator(token=token).validate_name(target=_input):
            _valid = True

        form[1].validation_result = _valid
        form[1].user_input = _input

        return render_template("partials/field.html", title="Register", field=form[1])

    @app.route("/v/email", methods=["POST"])
    def validate_email():
        _valid = False
        _input = request.form.get("lastName")

        if Validator(token=token).validate_email(target=_input):
            _valid = True

        form[2].validation_result = _valid
        form[2].user_input = _input

        return render_template("partials/field.html", title="Register", field=form[2])

    @app.route("/v/asset-name", methods=["POST"])
    def validate_asset_name():
        _valid = False
        _input = request.form.get("assetName")

        if Validator(token=token).validate_asset_name(target=_input):
            _valid = True

        form[3].validation_result = _valid
        form[3].user_input = _input

        return render_template("partials/field.html", field=form[3])

    @app.route("/v/phone-number", methods=["POST"])
    def validate_phone_number():
        _valid = False
        _input = request.form.get("phoneNumber")

        if Validator(token=token).validate_name(target=_input):
            _valid = True

        form[4].validation_result = _valid
        form[4].user_input = _input

        return render_template("partials/field.html", title="Register", field=form[4])

    @app.route("/v/imei-number", methods=["POST"])
    def validate_imei():
        _valid = False
        _input = request.form.get("imeiNumber")

        if Validator(token=token).validate_imei(target=_input):
            _valid = True

        form[5].validation_result = _valid
        form[5].user_input = _input

        return render_template("partials/field.html", title="Register", field=form[5])

    @app.route("/v/vin-number", methods=["POST"])
    def validate_vin():
        _valid = False
        _input = request.form.get("vinNumber")

        if Validator(token=token).validate_name(target=_input):
            _valid = True

        form[6].validation_result = _valid
        form[6].user_input = _input

        return render_template("partials/field.html", title="Register", field=form[6])

    return app


def validate(validator: Validator, data: dict) -> list[str | None]:
    results = validator.validate_all(data=data)
    bad_items = [key for key, value in results.items() if value is not True]
    return bad_items


if __name__ == "__main__":
    dotenv.load_dotenv()
    token = os.environ["WIALON_HOSTING_API_TOKEN_DEV"]
    app = create_app(token=token)
    app.run(debug=True)
