from flask import Flask, render_template, request
from auth import Session
from pprint import pprint
from wialon import Wialon, WialonError
import dotenv
import json
import os
import query

dotenv.load_dotenv()


def create_app(wialon_token: str | None):
    app = Flask(__name__)

    @app.route("/api/search", methods=['GET', 'POST'])
    def search():
        if request.method == 'GET':
            return render_template('search.html')
        elif request.method == 'POST':
            try:
                with Session(token=wialon_token) as session:
                    r = session.search_items(params=query.generate(request.form.get('search', '')))
                    response = json.dumps(r, indent=2, sort_keys=True)
                    return render_template('search-results.html', response=response)
            except WialonError as e:
                return(f'Error code {e._code}, msg: {e._text}')
        else:
            return render_template('index.html')

    @app.route("/api", methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            return render_template('index.html')
        else:
            # Retrive form data
            email = request.form.get('inputEmail', '')
            username = request.form.get('inputUsername', '')
            password = request.form.get('inputPassword', '')

            # Call Wialon API here with form data
            try:
                with Session(token=token) as session:
                    params = {
                        'creatorId': os.environ['WIALON_HOSTING_CREATOR_ID'],
                        'name': username,
                        'password': password,
                        'dataFlags': 1
                    }
                    response = session.create_user(params=params)
            except WialonError as e:
                return(f'Error code {e._code}, msg: {e._text}')

            return render_template(
                    'submit.html',
                    email=email,
                    username=username,
                    password=password,
                    response=response
                   )

    return app

if __name__ == "__main__":
    token = os.environ['WIALON_HOSTING_API_TOKEN_DEV']
    app = create_app(wialon_token=token)
    app.run(debug=True)