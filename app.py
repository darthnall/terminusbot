from flask import Flask, render_template, request
from auth.session import Session
from pprint import pprint
from wialon import Wialon, WialonError
import dotenv
import json
import os
from auth import PARAMETERS, query

dotenv.load_dotenv()


def create_app(wialon_token: str | None):
    app = Flask(__name__)

    @app.route("/api", methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            return render_template('index.html')
        else:
            # Retrive form data
            search_option = request.form.get('searchOption', '')
            keyword = request.form.get('inputKeyword', '')
            email = request.form.get('inputEmail', '')
            state = request.form.get('inputState', '')
            username = request.form.get('inputUsername', '')
            password = request.form.get('inputPassword', '')

            # Handle form data
            if search_option == 'Users':
                method = 'core/search_items'
                params = query(keyword)
                try:
                    with Session(token=token) as session:
                        response = session.call(method='core_search_items', params=params)
                except WialonError as e:
                    return(f'Error code {e._code}, msg: {e._text}\nparams: {params}')

            # Call Wialon API here with form data
            else:
                try:
                    with Session(token=token) as session:
                        params = PARAMETERS['core']['get_items_access']
                        response = session.call(method='get_items_access', params=params)
                except WialonError as e:
                    return(f'Error code {e._code}, msg: {e._text}\nparams: {params}')

            return render_template('response.html', response=response)

    return app

if __name__ == "__main__":
    token = os.environ['WIALON_HOSTING_API_TOKEN_DEV']
    app = create_app(wialon_token=token)
    app.run(debug=True)
