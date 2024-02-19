from flask import Flask, render_template, request
from auth.session import Session
from pprint import pprint
from wialon import Wialon, WialonError
import auth.query
import dotenv
import json
import os

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
                    keyword = request.form.get('search', '')
                    print(keyword)
                    category = request.form.get('searchType', '')
                    print(category)
                    response = session.search_items(params=auth.query.generate(keyword, category))
                    return render_template('search-results.html', response=response)
            except WialonError as e:
                return(f'Error code {e._code}, msg: {e._text}')
        else:
            return render_template('index.html')

    @app.route("/api/create-unit", methods=['GET', 'POST'])
    def create_unit():
        if request.method == 'GET':
            try:
                with Session(token=wialon_token) as session:
                    units = session.search_items(params=auth.query.generate('*', 'unit'))
                    return render_template('create-unit.html', units=units)
            except WialonError as e:
                return(f'Error code {e._code}, msg: {e._text}')
        elif request.method == 'POST':
            try:
                with Session(token=wialon_token) as session:
                    name = request.form.get('inputName', '')
                    imei = request.form.get('inputUnit', '')
                    t1000 = request.form.get('t1000', '')
                    params = {
                            "creatorId": int(os.environ['WIALON_HOSTING_CREATOR_ID_DEV']),
                            "name": name,
                            "hwTypeId": imei,
                            "dataFlags": 2

                            }
                    response = session.create_unit(params=params)
                    return render_template('create-unit-results.html', response=response)
            except WialonError as e:
                return(f'Error code {e._code}, msg: {e._text}, params={params}')
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
                        'creatorId': int(os.environ['WIALON_HOSTING_CREATOR_ID_DEV']),
                        'name': username,
                        'password': password,
                        'dataFlags': 2
                    }
                    response = session.create_user(params=params)
            except WialonError as e:
                return(f'Error code {e._code}, msg: {e._text}\nparams: {params}')

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
