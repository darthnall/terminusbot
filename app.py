from flask import Flask, render_template, request

def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            return render_template('index.html')
        else:
            print(request.form)
            email = request.form.get('inputEmail4', '')
            return render_template('submit.html', email=email)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
