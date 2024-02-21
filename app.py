# Wialon API session
from auth.session import Session
# Generate credentials for Wialon API
from client.create_user import gen_creds
from client.create_user import validate
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
def create_app(wialon_token: str | None):
    app = Flask(__name__)

    # Create /api route for Wialon API requests
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
                    creds = gen_creds(data=data)
                    response = session.create_user(creds=creds)
            except WialonError as e:
                return(f'Error code {e._code}, msg: {e._text}')

            return render_template('response.html', response=response, title='Response')

    return app

if __name__ == "__main__":
    # Load environment variables
    dotenv.load_dotenv()
    token = os.environ['WIALON_HOSTING_API_TOKEN_DEV']
    app = create_app(wialon_token=token)
    app.run(debug=True)
