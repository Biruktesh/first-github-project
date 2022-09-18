from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///friends.db"
db = SQLAlchemy(app)


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def repr(self):
        return "Name %r" % self.id


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == "POST":
        friend_to_update.name = request.form["name"]

        try:

            db.session.commit()
            return redirect("/friends")
        except:
            return "error with th data base :("
    else:

        return render_template("update.html", friend_to_update=friend_to_update)


@app.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)

    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect("/friends")
    except:
        return "error with th data base :("


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/creator")
def creator():
    return render_template("creator.html")



@app.route("/form", methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    return render_template("form.html", first_name=first_name, last_name=last_name, email=email, password=password)


@app.route("/friends", methods=["POST", "GET"])
def friends():
    if request.method == "POST":
        friend_name = request.form["name"]
        new_f = Friends(name=friend_name)
        try:
            db.session.add(new_f)
            db.session.commit()
            return redirect("/friends")
        except:
            return "error with th data base :("
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template("friends.html", friends=friends)


db.create_all()
app.run()