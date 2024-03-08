from auth import Session, Validator
from client import Unit, User, create_new_form, create_validated_form

from client.formdata import create_validated_form
from flask import Flask, render_template, request

import dotenv
import json
import os


def create_app(token: str):
    app = Flask(__name__)


    @app.route("/", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            imei = ""
            if request.args.get("imei"):
                imei = request.args.get("imei")

            data = create_new_form(
                firstName = { "valid": None, "target": "" },
                lastName = { "valid": None, "target": "" },
                email = { "valid": None, "target": "" },
                assetName = { "valid": None, "target": "" },
                phoneNumber = { "valid": None, "target": "" },
                vin = { "valid": None, "target": "" },
                imei = { "valid": None, "target": f"{imei}" },
                testValue = { "valid": None, "target": "" },
            )

            return render_template("register.html", title="Registration", data=data)

        elif request.method == "POST":
            data = request.form
            page = "register.html"

            # Handle validation
            validation_results = Validator(token=token).validate_all(data=data)
            bad_items = [key for key, value in validation_results.items() if value is not True]
            print(f"{ data = }")
            if bad_items:
                return render_template("register.html", title="Invalid", data=data)

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

    @app.route("/v/test-value", methods=["POST"])
    def validate_test_value():
        _valid = False
        data = { "testValue": request.form.get("testValue") }


        if Validator(token=token).validate_test(target=data["testValue"]):
            _valid = True

        response = json.dumps({
            "testValue": {
                "valid": _valid,
                "target": data["testValue"]
            }
        }), 200, {"Content-Type": "application/json"}

        return response


    @app.route("/v/first-name", methods=["POST"])
    def validate_first_name():
        _valid = False
        data = { "firstName": request.form.get("firstName") }


        if Validator(token=token).validate_name(target=data["firstName"]):
            _valid = True

        response = json.dumps({
            "firstName": {
                "valid": _valid,
                "target": data["firstName"]
            }
        }), 200, {"Content-Type": "application/json"}

        # TODO: Add logging

        return response


    @app.route("/v/last-name", methods=["POST"])
    def validate_last_name():
        _valid = False
        data = { "lastName": request.form.get("lastName") }


        if Validator(token=token).validate_name(target=data["lastName"]):
            _valid = True

        response = json.dumps({"lastName": { "valid": _valid, "target": data["lastName"] }})

        return response


    @app.route("/v/email", methods=["POST"])
    def validate_email():
        _valid = False
        data = { "email": request.form.get("lastName") }


        if Validator(token=token).validate_name(target=data["email"]):
            _valid = True

        response = json.dumps({"email": { "valid": _valid, "target": data["lastName"] }})

        return response


    @app.route("/v/asset-name", methods=["POST"])
    def validate_asset_name():
        _valid = False
        data = { "assetName": request.form.get("assetName") }


        if Validator(token=token).validate_name(target=data["assetName"]):
            _valid = True

        response = json.dumps({"assetName": { "valid": _valid, "target": data["assetName"] }})

        return response


    @app.route("/v/phone-number", methods=["POST"])
    def validate_phone_number():
        _valid = False
        data = { "phoneNumber": request.form.get("phoneNumber") }


        if Validator(token=token).validate_name(target=data["phoneNumber"]):
            _valid = True

        response = json.dumps({"phoneNumber": { "valid": _valid, "target": data["phoneNumber"] }})

        return response


    @app.route("/v/imei", methods=["POST"])
    def validate_imei():
        _valid = False
        data = { "imei": request.form.get("imei") }


        if Validator(token=token).validate_imei(target=data["imei"]):
            _valid = True

        response = json.dumps({"imei": { "valid": _valid, "target": data["imei"] }})

        return response


    @app.route("/v/vin", methods=["POST"])
    def validate_vin():
        _valid = False
        data = { "vin": request.form.get("vin") }


        if Validator(token=token).validate_name(target=data["vin"]):
            _valid = True

        response = json.dumps({"vin": { "valid": _valid, "target": data["vin"] }})

        return response


    return app


if __name__ == "__main__":
    dotenv.load_dotenv()
    token = os.environ["WIALON_HOSTING_API_TOKEN_DEV"]
    app = create_app(token=token)
    app.run(debug=True)
