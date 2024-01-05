import os
import csv
import datetime
import flask_sqlalchemy
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import LoginManager, UserMixin, login_required
from flask_session import Session
from flask import Response
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import pytz
import requests
import subprocess
import urllib
import uuid
import statistics
from statistics import mean
from operator import itemgetter


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Configuration of the flask application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "mysecretkey"
Session(app)

## Database for FAST is in the /workspaces/87627785/project/FAST/db path
db = SQL("sqlite:///db/FAST.db")

@app.route("/")  ##index route
@login_required
def index():

    user_id = session["user_id"]
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"]) #loginroute
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted  ##return an apology("must provide username", 403)
        if not request.form.get("username"):
             flash("must provide a username", 403)
             return redirect("/login")
        # Ensure password was submitted ## return an apology("must provide password", 403)

        elif not request.form.get("password"):
             flash("must provide a passwrod", 403)
             return redirect("/login")
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct ##  return apology("invalid username and/or password", 403)

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
           flash("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"]) #registert route
def register():
    """Register user"""  ### creating a function to create/register new user for the App.
    if (
        request.method == "GET"
    ):  ## if the user is just clicking on the request buttons on the pages (GET)
        return render_template("register.html")  ## then just render the get page
    else:  ## if the user instead is using any of fields on form to post, (POST) then:
        username = request.form.get("username")
        password = request.form.get("password")
        confirma = request.form.get("confirmation")
        ## create variables to hold user inputs from registerdothtml
        if not username:
             flash("Username must be provided", 403)
             return render_template("register.html")

        if not password:
            flash("Password must be provided", 403)
            return render_template("register.html")
            ## same idea as above but for password
        if not confirma:
            flash("Password confirmation did not match", 403)
            return render_template("register.html")
            ## same idea as above but for password again

        if password != confirma:  ## user must input the password exactly the same way twice
            flash("password confirmation did not match", 403)
            return render_template("register.html")## use the "apology function" to provide instructions to user

        hash = generate_password_hash(confirma)  ## this function is already provided as an imported library, see line 6 of python header
        try:  ## we are going to "try" to see if inserting value into the tableis valid. meaning, if a user with that same name does not already exists.
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
            )  ## acess the data base variable (line 22) and use SQL scrip to instert new user into table "users"
        except:  ## what happens if the user name matches an existing one in the data base ?
                flash("Username already exists", 403)
                return render_template("register.html")
                ##aplogize render page with message
        session["user_id"] = user_id
    return redirect("/")  ### get back to the main page with the session enabeled

@app.route("/logout") #logout route
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/create", methods=["POST", "GET"]) ## create route
@login_required
def create():
    if request.method == 'POST': ## html page uses a from
        try:
            # Retrieve form's input data
            event_name = request.form.get('eventName')
            event_date = request.form.get('eventDate')
            sport = request.form.get('sport')
            competitor_count = request.form.get('competitorCount')
            judge_count = int(request.form.get('judgecount'))
            judge_names = [request.form.get(f'judgeName{i+1}') for i in range(judge_count)]
            runs = request.form.get('runs')
            jaggregatekind = request.form.get('jaggregatekind')
            scoring_type = request.form.get('scoringtype') ## all of theabove are variables obtained from the form
            checkjudge_query1 = db.execute("SELECT username FROM users")
            checkjudge = [row['username'] for row in checkjudge_query1]
            checkjudge_query2 = db.execute("SELECT id, username FROM users")
            checkjudge_data = [(row['id'], row['username']) for row in checkjudge_query2]
            checkjudge_ids = [user_id for user_id, username in checkjudge_data if username in checkjudge]
            ##print("Judge Names:", judge_names) ## debugger
            ##print("users:", checkjudge) ## debugger
            ##print("usersid:", checkjudge_ids) ## debugger
            session['seshcompcount'] = int(competitor_count)
            session['seshjudgcount'] = int(judge_count)
            session['secheventname'] = event_name
            session['sechruncounts'] = int(runs)
            session['sechscoretype'] = scoring_type
            session['jdgaggregtion'] = jaggregatekind

            for judge_name in judge_names:
                if judge_name not in checkjudge:
                    # Judge name does not exist in the users table
                    flash(f"Judge name '{judge_name}' does not exist.", category='error')
                    return redirect("/create")

            for jdgid in checkjudge_ids:
                db.execute(
                    "INSERT INTO events (eventname, date, sport, competitorcount, judgecount, runs, jaggregatekind, scoringtype, judge_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    event_name, event_date, sport, competitor_count, judge_count, runs, jaggregatekind, scoring_type, jdgid
                    )# Redirect to some page after successful submission

            return render_template("enrollment.html", event_name = event_name, judge_count = int(judge_count), competitor_count = int(competitor_count))
           ###return redirect(url_for('enrollment', event_name=event_name, judge_count=int(judge_count), competitor_count=int(competitor_count)))
           ## redirect user to the enroll page and pass nescesary info to rout using session

        except Exception as e:
            flash(f"Error: {e}", 500)  # Show a generic error message
            return redirect("/")
    else:
        return render_template("create.html")


@app.route("/enrollment", methods=["GET", "POST"])
@login_required
def enrollment():
    # Handle GET and POST requests for the enrollment form
    if request.method == 'POST':
        def copy(value):
            new = value
            return(new)
        ##judge_count = copy(gjudge)
        ##print("copy ", judge_count)
        competitor_count = session.get('seshcompcount', 0)
        judge_count = session.get('seshjudgcount',0)
        event_name = session.get('secheventname', 0)
        ## print("competitors:", competitor_count)
        print("event:",event_name)
        session['sccscompcount'] = int(competitor_count)
        session['sccsjudgcount'] = int(judge_count)
        session['sccseventname'] = event_name
        if competitor_count is not None:
            try:
                competitor_count_in = int(competitor_count)
            except ValueError:
                # Handle the case where the value is not a valid integer
                flash("Invalid value for competitor_count.", category='error')
                return redirect('/error-page')  # Replace with the desired error page URL or template
        else:
            # Handle the case where the value is None
            flash("Competitor count is missing.", category='error')
            return redirect('/error-page')  # Replace with the desired error page URL or template

        # Process the competitor enrollment form data
        for i in range(competitor_count):
            competitor_name = request.form.get(f'name{i + 1}')
            competitor_nick = request.form.get(f'nick{i + 1}')
            competitor_age = request.form.get(f'age{i + 1}')
            competitor_origin = request.form.get(f'origin{i + 1}')
            print(competitor_name, competitor_nick, competitor_age, competitor_origin, event_name, judge_count)

            # Insert data into the database or perform necessary actions
            db.execute(
                "INSERT INTO competitors (name, nick, age, origin, eventname, evaluators) VALUES (?, ?, ?, ?, ?, ?)",
                competitor_name, competitor_nick, competitor_age, competitor_origin, event_name, judge_count
            )

        # Redirect to success page or handle errors
        flash("Enrollment successful!", category='success')
        return render_template("success.html", event_name = event_name, judge_count = int(judge_count), competitor_count = int(competitor_count))

    # Redirect to some page after successful submission
    return render_template("enrollment.html", event_name = event_name, judge_count = int(judge_count), competitor_count = int(competitor_count))

@app.route("/success", methods=["GET"])
@login_required
def success():
    if request.method == 'GET':
        competitor_count = session.get('seshcompcount', 0)
        judge_count = session.get('seshjudgcount',0)
        event_name = session.get('secheventname', 0)

        return render_template("success.html")


@app.route("/eventscore", methods=["GET", "POST"])
@login_required
def eventscore():
    if request.method == 'GET':
        event_name = session.get('secheventname', 0)
        judge_count = session.get('seshjudgcount', 0)
        competitor_count = session.get('seshcompcount', 0)
        runs = session.get('sechruncounts',0)
        jaggregatekind = session.get('jdgaggregtion',0)
        scoring_type = session.get('sechscoretype',0)
        # Query the database for competitor records with the same event name
        competitors_data = db.execute("SELECT name FROM competitors WHERE eventname = ?", event_name)
        # Prepare a list of dictionaries with competitor names
        competitors_list = [{'name': row['name']} for row in competitors_data]

        return render_template("eventscore.html", event_name=event_name, judge_count=judge_count, competitor_count=competitor_count, competitors=competitors_list, runs=runs, jaggregatekind=jaggregatekind, scoring_type=scoring_type )

    else:
        event_name = session.get('secheventname', 0)
        try:
            competitors_data = db.execute("SELECT name FROM competitors WHERE eventname = ?", event_name)
            competitors_list = [{'name': row['name']} for row in competitors_data]  ##ended up unused ## print("list", competitors_list)
            namesnames = [row['name'] for row in competitors_data]
            print("event:",event_name)
            print(namesnames)
            competitor_count = session.get('seshcompcount', 0)
            compnames = [request.form.get(f'compname{i + 1}') for i in range(competitor_count)]  ##ended up unused
            print("comp names", compnames)
            ## scores_per_competitor = [request.form.getlist(f'scores{i + 1}[]') for i in range(competitor_count)]
            scores_per_competitor = [request.form.getlist(f'scores{i}') for i in range(1, competitor_count + 1)]
            print(scores_per_competitor)
            final_scores = calculate_final_scores(scores_per_competitor)

            for nname, final_score in zip(namesnames, final_scores):
                  update_competitor_score(nname, event_name, final_score)
            flash("Your event's results are ready!")
            return redirect(url_for('results'))

   ### return render_template("eventscore.html", event_name=event_name, competitor_count=competitor_count)

        except Exception as e:
            flash(f"Error: {e}", 500)  # Show a generic error message
            return redirect("/")

    return render_template("eventscore.html", event_name=event_name, competitor_count=competitor_count)


def calculate_final_scores(scores_per_competitor):
    # Process scores based on the chosen scoring type
    scoring_type = session.get('sechscoretype', 0)
    final_scores = []

    for scores in scores_per_competitor:
        if scoring_type == "TotalSum":
            final_score = sum(map(float, scores))
        elif scoring_type == "TotalAverage":
            final_score = mean(map(float, scores))
        elif scoring_type == "BestRun":
            final_score = max(map(float, scores))
        else:
            final_score = sum(map(float, scores))

        final_scores.append(final_score)

    return final_scores

def update_competitor_score(compname, event_name, final_score):
    # U
     db.execute("UPDATE competitors SET currentscore = ? WHERE name = ? AND eventname = ?", final_score, compname, event_name)
def add_score_to_competitor(name, new_scores):
    """
    Add new scores for a competitor.
    """
    competitor = db.execute("SELECT * FROM competitors WHERE name = ? AND eventname = ?", name, event_name).fetchone()
    current_scores = competitor['current_scores']
    # U
    updated_scores = current_scores + ",".join(new_scores)
    # U
    db.execute("UPDATE competitors SET current_scores = ? WHERE name = ? AND eventname = ?", updated_scores, name, event_name)


@app.route("/results", methods=["GET"])
@login_required
def results():
    event_name = session.get('secheventname', 0)
    judge_count = session.get('seshjudgcount', 0)
    competitor_count = session.get('seshcompcount', 0)
    runs = session.get('sechruncounts',0)
    jaggregatekind = session.get('jdgaggregtion',0)
    scoring_type = session.get('sechscoretype',0)
    competitors_data = db.execute("SELECT name, currentscore FROM competitors WHERE eventname = ?", event_name)     # this will query the db for competitor records with the same event name

    competitors_list = [{'name': row['name'], 'currentscore': row['currentscore']} for row in competitors_data]        # makes a tuple with competitor names and scores

    sorted_competitors = sorted(competitors_list, key=itemgetter('currentscore'), reverse=True)      # Sorts the list of competitors based on their current scores in descending order, needed to import itemgetter from operator library

    csv_data = generate_csv_data(sorted_competitors)

    response = Response(csv_data, content_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={event_name}_results.csv"

    ##return response
    return render_template("results.html", competitors=sorted_competitors, event_name=event_name)

def generate_csv_data(competitors):
    csv_data = "Competitor,Score\n"
    for competitor in competitors:
        csv_data += f"{competitor['name']},{competitor['currentscore']}\n"
    return csv_data

@app.route("/about", methods=["GET"])
def about():
    if (request.method == "GET"):
         return render_template("about.html")
