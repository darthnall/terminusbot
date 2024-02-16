from flask import Flask

def main():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello World!"

if __name__ == "__main__":
    main()
