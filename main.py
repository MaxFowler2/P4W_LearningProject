from flask import Flask
from flask import render_template
from flask import request

import database_interface

# Global variables
is_logged_in = False


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
@app.route("/parameters.html", methods=["GET"])
def parameters_page():
    # Access the request object to get the value of the URL parameter
    # If the URL parameter isn't in the URL string, then set the value to "default"
    pageVer = request.args.get("ver", "default")

    return render_template("parameters.html", pageVersion=pageVer), 200


@app.route("/products.html", methods=["GET"])
def product_page():
    data = database_interface.listExtension()
    return render_template("products.html", content=data), 200


@app.route("/index.html", methods=["GET", "POST"])
def index_page():
    global is_logged_in
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        is_logged_in = database_interface.check_login(email, password)

        if is_logged_in:
            print(f"user {email} has logged in with {password}")
        else:
            print(f"user {email} failed to log in with {password}")
    else:
        is_logged_in = False
    return render_template("index.html", logged_in=is_logged_in), 200


if __name__ == "__main__":
    app.run(debug=True)
