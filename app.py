# Wialon API session
from auth import Session
# Generate credentials for Wialon API
from client import User
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
    def index():
        if request.method == 'GET':
            return render_template('register.html', title='Registration')
        else:
            # Collect form data
            data = request.form
            # Pass form data to Wialon API
            try:
                with Session(token=token) as session:
                    creds = {
                             'username': 'blake.nall',
                             'password': '123',
                             'email': 'blakenall@proton.me',
                             'phoneNumber': '17133049421',
                             'imei': 123
                             }
                    user = User(creds=creds, session=session)
                    print(user.email)
                    return render_template('response.html', response=creds, title='Response', redirect='register')
            except WialonError as e:
                return(f'Error code {e._code}, msg: {e._text}')

            return render_template('response.html', response=response, title='Response', redirect='register')

    if debug_mode_enabled:
        @app.route("/token", methods=['GET'])
        def token_list():
            with Session(token=token) as session:
                response = session.token_list()
                return render_template('response.raw.html', response=response, title='Tokens', redirect='token')

        # TODO: Write this function
        endpoint = 'search'
        @app.route(f"/{endpoint}", methods=['GET', 'POST'])
        def search_items():
            if request.method == 'GET':
                return render_template('response.html', title='Search', redirect=endpoint)
            else:
                return render_template('response.html', title='Search', redirect=endpoint)

        @app.route("/resource", methods=['GET', 'POST'])
        def resource():
            if request.method == 'GET':
                with Session(token=token) as session:
                    # Do some stuff
                    response = session.set_sms(user_id=27881459)
                    return render_template('response.raw.html', response=response, title='Resource', redirect='resource')
            else:
                return render_template('response.html', title='Resource', redirect='resource', response=None)

    return app

if __name__ == "__main__":
    # Load environment variables
    dotenv.load_dotenv()
    token = os.environ['WIALON_HOSTING_API_TOKEN_DEV']
    app = create_app(token=token)
    app.run(debug=True)
