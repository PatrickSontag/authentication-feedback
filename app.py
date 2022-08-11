"""Example flask app that stores passwords hashed with Bcrypt. Yay!"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Show homepage with links to site areas."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first = form.first_name.data
        last = form.last_name.data

        user = User.register(name, pwd, email, first, last)
        db.session.add(user)
        db.session.commit()

        flash('Successfully Created New Account')

        session["username"] = user.username

        # on successful login, redirect to secret page
        return redirect(f"/user/{user.username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, pwd)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/user/{username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
# end-login


@app.route("/user/<username>")
def user(username):
    """Example hidden page for logged-in users only."""

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")


    else:
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter_by(user_id=username)

        return render_template("user.html", username=username, user=user, feedback=feedback)

@app.route("/user/<username>/delete", methods=["POST"])
def delete_user(username):
    """Remove user from database."""
    session.pop("username")

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("username")

    return redirect("/")

@app.route("/user/<username>/feedback/add", methods=["GET"])
def add_feedback_form(username):
    """Add feedback to database."""

    form = FeedbackForm()
    user = User.query.get_or_404(username)
    

    return render_template("feedback.html", form=form, user=user)

@app.route("/user/<username>/feedback/add", methods=["POST"])
def add_feedback(username):
    """Add feedback to database."""
    form = FeedbackForm()

    title = form.title.data
    feedback = form.content.data

    feedback = Feedback(title=title, content=feedback, username=username)
    db.session.add(feedback)
    db.session.commit()

    return redirect (f"/user/{username}")

@app.route("/feedback/<feedback_id>/update", methods=["GET"])
def edit_feedback(feedback_id):
    """Edit feedback by feedback id"""
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    username = session["username"]
    user = User.query.get_or_404(username)

    # return render_template("feedback.html", form=form)
    return render_template("edit_feedback.html", form=form, user=user, feedback_id=feedback_id)

@app.route("/feedback/<feedback_id>/update", methods=["POST"])
def update_feedback(feedback_id):
    """Update feedback"""
    form = FeedbackForm()

    title = form.title.data
    feedback = form.content.data
    user_id = session["username"]

    old = Feedback.query.get(feedback_id)
    db.session.delete(old)

    fb = Feedback(title=title, content=feedback, user_id=user_id)
    db.session.add(fb)
    db.session.commit()

    return redirect (f"/user/{user_id}")

