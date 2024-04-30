from auth import Session, Validator, Searcher
from client import Unit, User
from client.form import create_registration_form

from datetime import datetime

from webhooks import TwilioCaller, create_message

from flask import Flask, render_template, request, jsonify
from flask import session as flask_session

from config import Config


def create_app():
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY
    app.config["SESSION_TYPE"] = "filesystem"

    @app.route("/emailsignup", methods=["GET", "POST"])
    def emailsignup():
        if request.method == "GET":
            return render_template("emailsignup.html")
        if request.method == "POST":
            success = False
            email = request.form.get("email")
            consent = bool(request.form.get("consent"))

            if consent:
                print(f"{datetime.now()} - {email = }")
                success = True

            return render_template("partials/emailsignup.html", email=email, success=success)
        else:
            return "404"

    @app.route("/notify", methods=["GET", "POST"])
    def notify():
        if request.method == "GET":
            return jsonify({"status": "success", "msg": "GET method not implemented."})

        elif request.method == "POST":
            caller = TwilioCaller()
            alert_type = request.form.get('alert_type')

            to_number, msg = create_message(alert_type=alert_type, data=request.form)

            try:
                if isinstance(to_number, list):
                    caller.batch_send(to_number, msg)
                    status = "success"
                else:
                    caller.send(to_number, msg)
                    status = "success"
            except ValueError:
                status = "failure"

            return jsonify({"status": status, "phone": to_number})
        else:
            pass

    @app.route("/", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            form = create_registration_form()
            flask_session["REGISTRATION_FORM"] = form

            form["imeiNumber"].user_input = request.args.get("imei")

            return render_template(
                "register.html", title="Registration", form=form, success=None
            )

        elif request.method == "POST":
            form = flask_session["REGISTRATION_FORM"]
            data = request.form
            success = False
            title = "Failure"

            bad_items = Validator().validate_all(data=data)

            if len(bad_items) == 0:
                success = True
                title = "Success!"

            if success:
                with Session() as session:
                    user = User(data=data, session=session)
                    user.create(
                        name=user.creds["email"], password=user.creds["password"]
                    )
                    print("Created user in Wialon")

                    unit = Unit(
                        imei=user.creds["imeiNumber"],
                        name=user.creds["assetName"],
                        session=session,
                    )
                    unit.assign(user_id=user.creds["userId"])
                    print("Created unit in Wialon and assigned to user")

                    if user.email_creds():
                        print("Email sent successfully")

            # Reset the form after submission
            form = create_registration_form()
            flask_session["REGISTRATION_FORM"] = form
            return render_template(
                "register.html",
                title=title,
                form=form,
                success=success,
                bad_items=bad_items,
            )

        else:
            return "404"

    @app.route("/v/first-name", methods=["POST"])
    def validate_first_name():
        field = flask_session["REGISTRATION_FORM"]["firstName"]
        _valid = False
        _input = request.form.get("firstName")

        _valid, _msg = Validator().validate_name(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/last-name", methods=["POST"])
    def validate_last_name():
        field = flask_session["REGISTRATION_FORM"]["lastName"]
        _valid = False
        _input = request.form.get("lastName")

        _valid, _msg = Validator().validate_name(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/email", methods=["POST"])
    def validate_email():
        field = flask_session["REGISTRATION_FORM"]["email"]
        _valid = False
        _input = request.form.get("email")

        _valid, _msg = Validator().validate_email(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/asset-name", methods=["POST"])
    def validate_asset_name():
        field = flask_session["REGISTRATION_FORM"]["assetName"]
        _valid = False
        _input = request.form.get("assetName")

        _valid, _msg = Validator().validate_asset_name(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/phone-number", methods=["POST"])
    def validate_phone_number():
        field = flask_session["REGISTRATION_FORM"]["phoneNumber"]
        _valid = False
        _input = request.form.get("phoneNumber")

        _valid, _msg = Validator().validate_phone_number(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/imei-number", methods=["POST"])
    def validate_imei():
        field = flask_session["REGISTRATION_FORM"]["imeiNumber"]

        _valid = False
        _input = request.form.get("imeiNumber")

        _valid, _msg = Validator().validate_imei_number(target=_input)

        print(f"{_valid = } {_msg = } {_input = }")

        update_field(field=field, data=(_valid, _msg, _input))

        return render_template("partials/field.html", title="Register", field=field)

    @app.route("/v/vin-number", methods=["POST"])
    def validate_vin():
        field = flask_session["REGISTRATION_FORM"]["vinNumber"]

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
