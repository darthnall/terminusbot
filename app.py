# Wialon API session
from auth import Session
# Generate credentials for Wialon API
from client import User
from client import Unit
# Flask webapp for handling requests
from flask import Flask
from flask import render_template
from flask import request
# Print the data in human readable format
from pprint import pprint
# Wialon API wrapper by Wialon
from wialon import Wialon
from wialon import WialonError
# Environment variables and i/o
import dotenv
import json
import os

# Create a Flask app
def create_app(token: str | None, debug_mode_enabled: bool = True):
    app = Flask(__name__)

    # Create /register route for Wialon API requests
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            try:
                imei = request.args.get('imei')
            except KeyError:
                imei = None
            return render_template('register.html', title='Registration', imei=imei)
        else:
            data = request.form
            try:
                with Session(token=token) as session:
                    user = User(data=data, session=session)
                    user.create()

                    unit = Unit(data=data, session=session)
                    response = unit.assign(user_id=user.id)

                    if data['vin']:
                        unit.set_vin(data['vin'])
            except WialonError as e:
                return(f'Error code {e._code}, msg: {e._text}')

            if type(response) == list:
                return render_template('response.raw.html', response=response, title='Response', redirect='register')
            else:
                return render_template('response.html', response=response, title='Response', redirect='register')

    return app

if __name__ == "__main__":
    # Load environment variables
    dotenv.load_dotenv()
    token = os.environ['WIALON_HOSTING_API_TOKEN_DEV']
    app = create_app(token=token)
    app.run(debug=True)
