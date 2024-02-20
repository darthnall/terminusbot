# Wialon API session
from auth.session import Session
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
    @app.route("/api", methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            return render_template('index.html')
        else:
            # Retrive form data
            search_option = request.form.get('searchOption', '')
            keyword = request.form.get('inputKeyword', '')

            # Handle form data
            if search_option == 'Users':
                try:
                    with Session(token=token) as session:
                        response = session.search(keyword=keyword, category='user')
                except WialonError as e:
                    return(f'Error code {e._code}, msg: {e._text}\nparams: {params}')

            # Call Wialon API here with form data
            else:
                try:
                    with Session(token=token) as session:
                        response = session.create_user(username=username, password=password)
                except WialonError as e:
                    return(f'Error code {e._code}, msg: {e._text}')

            return render_template('response.html', response=response)

    @app.route("/api/create", methods=['GET', 'POST'])
    def create():
        if request.method == 'GET':
            return render_template('create.html')
        else:
            opt = request.form.get('createOption', '')
            email = request.form.get('inputEmail', '')
            username = request.form.get('inputUsername', '')
            password = request.form.get('inputPassword', '')
            address = request.form.get('inputAddress', '')
            state = request.form.get('inputState', '')
            try:
                with Session(token=token) as session:
                    response = session.create_user(username=username, password=password)
            except WialonError as e:
                return(f'Error code {e._code}, msg: {e._text}')

            return render_template('response.html', response=response)
        return render_template('response.html', response=None)

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        else:
            email = request.form.get('inputEmail', '')
            username = request.form.get('inputUsername', '')
            password = request.form.get('inputPassword', '')
            address = request.form.get('inputAddress', '')
            state = request.form.get('inputState', '')


    return app

if __name__ == "__main__":
    # Load environment variables
    dotenv.load_dotenv()
    token = os.environ['WIALON_HOSTING_API_TOKEN_DEV']
    app = create_app(wialon_token=token)
    app.run(debug=True)
