import requests

from client.form import create_registration_form
from config import Config
from flask import (
    Flask,
    render_template,
    request,
)


def create_app():
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SECRET_KEY=Config.SECRET_KEY,
    )
    app.config.from_object(__name__)

    @app.route("/", methods=["GET", "POST"])
    def register():
        if request.args and request.method == "GET":
            form = create_registration_form(request.args.get("imei"))
        else:
            form = create_registration_form(None)

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
                "https://api.terminusgps.com/v1/forms/wialon/create_user", params=params
            )

            return render_template(
                "register.html",
                title="Register",
                success=True,
                form=form,
            )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
