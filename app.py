from flask import Flask, render_template, request
from auth import Session
from pprint import pprint
from wialon import Wialon, WialonError
import dotenv
import os

dotenv.load_dotenv()


def create_app(wialon_token: str | None):
    app = Flask(__name__)

    @app.get("/get")
    def account():
        try:
            with Session(token=wialon_token) as session:
                params = {
                'spec': {
                    'itemsType': 'user',
                    'propName': 'sys_name,sys_id',
                    'propValueMask': '*',
                    'sortType': 'sys_name'
                        },
                'force': 1,
                'flags': 1,
                'from': 0,
                'to': 0
                }
                response = session.search_items(params=params)
                return render_template('get.html', response=response)
        except WialonError as e:
            return(f'Error code {e._code}, msg: {e._text}')

    @app.route("/", methods=['GET', 'POST'])
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
