# FAST--Score-Keeper-
FAST-sk is Web App for fully scoring a Freestyle Action Sport competition (BMX, Skateboarding, MTB Slopestyle, Snowboard, dancing. etc.) where an “Event” gets created, “Competitors” get enrolled, “Judges” log-in for scoring and by the time scoring and the event itself concludes, the program ultimately outputs the Final Results of the competition.

#### Video Demo:  https://youtu.be/WcE1PW-iOUg

#Problem to be solved :
Currently in my local BMX scene (Republic of Panamá) whenever there’s a BMX freestyle competition the scoring gets carried out in a very archaic and inconvenient method: PEN AND PAPER !!! My goal is to create a better solution for whenever there’s an event scoring need.

#What will this software do?
Input: Judges for an action sport competiton would log in (they are the users) and "Create an Event", they will set parameters for said event, register competiors, and ultimately submit scores for each competitor.
Output: After an event is created, the program presents a table style form for the judges to easily submit their scores, and after every score is submitted, the program finally returns the results of the competition and the standings.

##Side Note: What will it not do ?
This program will not produce or generate an individual run score for the judge.
In freestyle action sports, judges scores are fully arbitrary and the score awarded very much up to the judge.
Each judge will subjectively decide what scores will the competitor gets each run, and input that number into the program. The performance of each rider is judged on overall impression.
So it's up to the judge/user/human to decide what score they award each rider.


#How will it be executed?
Upon dreaming up this project, I established that the main Functionality of the FAST Program needs to be as follows:
1. Needs to be able to create an “event”
2. Needs to be able to enroll “competitors”
3. Needs to be able to enroll “Judges”
4. Needs to be able to record the score each Judge per “competitor”
5. Needs to be able to aggregate all judges score for each competitors
6. Needs to determine Winner, second and Third place for event.
7. Create CSV file with results.

##Optional Future Wishlist
- produce a final ranking/standings list.
- Public Live Feed ?
- Creation of Brackets and heats ?
- Creation of Qualifiers and Finals ?
- Expand into a Circuit score / points trackers across multiple events

###Building Blocks
- HTML for the page
- CSS for the look (Bootstrap)
- JS for the front end
- Flask for the Back end handling
- SQL for the event competitor list
- Python for logic

##Features:
- Flexibility: FAST adapts to the unique scoring requirements of different events and sports. Customize scoring types, aggregate methods, and more to suit your needs.
- User Management: Create accounts for judges and administrators, allowing for a collaborative and organized scoring process.
- Event Creation: Easily set up new events, specifying the number of competitors, judges, and scoring parameters.
- Real-time Scoring: Judges can submit scores in real-time, and the system calculates final scores dynamically.
- Results Generation: View detailed results, rankings, and standings for each event. Export results to CSV for further analysis.

##User Overview:
-Create an Account: Judges and administrators can create accounts on the FAST platform.
-Event Setup: Set up a new event by providing details such as event name, date, sport, competitor count, and judge count.
-Competitor Enrollment: Enroll competitors in the event, capturing essential details like name, age, and origin.
-Scoring: Judges input scores for each competitor, and FAST calculates final scores based on the chosen scoring type.
-Results: Explore detailed event results, including individual scores, rankings, and overall standings.


#Here are some key definitions:

**Judges:** these are going to be the users of the application. they will have to
log into a session in and be registered to an ”event” in order to judge.
They can also create an “event” and register “competitors”.

**Competitors:** these are the who the judges will provide a score for.
Competitors should have an Id, Name, Nick name, Age, Region, time
stamp of when they registered for the event and a score or scores
in the data base (maybe a standings/rankings as well)

**Event:** this will be a title or a tag for each separate competition
in the data base. When a judge look’s up or work’s on an event, the
user should see only the competitors registered to that specific event
available to score. Events might have a separated table in the data base
with: Event name, date, Category/sport, count of registered competitors,
count of judges who will be scoring, runs (defined below), run time,
aggregation type (defined below ) scoring type (defined below).

**Run:** in action sports, athletes have a timed run of x amount of **seconds** 
to use to perform for the judges. During that timed run, they do as much
as possible to impress the judges.

**Aggregation type:** this will define how we will add up the score of the
judges per competitor, per run. We can either sum up all scores from all
judges and the summary of these scores is the score for that competitor
for that run, or we do an average of all judges scores for that same run.
The scope of this version of FAST will handle summary only.

**Scoring type:** run by run, all judges contribute to one competitor’s score
for that run. if there is a second, third, or other amounts of runs, the
scoring type determines if the competitor will get an aggregation/sum of
all runs for a final score, ,an average of all scores or (more commonly)
the best or highest number of all provided score is what is determined
to be a final score.

##File structure:
Since this program was build using the Flask/Jinja convetions, the filing system for files in this web ap follow the conventional lay out of any flask application, with a templates folder for html, a static folder for css styles and images, a db directory for the databas and an app.py file wher all the logic of the program takes place
Specific to this web app, the file structure will look like the bellow diagram

  - /FAST:
   -----/app.py
   -----/db:
   --------/FAST.db
   -----/static:
   -------/images:
   ----------/ images the web app uses
   -----/styles.css
   -----/templates:
   --------/about.html
   --------/create.html
   --------/enrollment.html
   --------/events.html
   --------/eventscore.html
   --------/index.html
   --------/login.html
   --------/register.html
   --------/results.html
   --------/success.html
   -----/config.py
   -----/style.js
   -----/requirements.txt


##Database Setup:

Created a database model for Judges (users), Competitors, Events a activity log within the db folder called FAST.db.
Each table definition is structured with logical column names and data types.Foreign key constraints are set to reference the primary keys in other tables.
Find below the main table schemas and also relationships between these models, considering that an Event has multiple Competitors and Judges.

-- users table (users are Judges)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

-- events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eventname TEXT NOT NULL,
    date DATE,
    sport TEXT NOT NULL,
    competitorcount INTEGER NOT NULL,
    judgecount INTEGER NOT NULL,
    runs INTEGER NOT NULL,
    jaggregatekind TEXT NOT NULL,
    scoringtype TEXT NOT NULL,
    judge_id INTEGER,
    FOREIGN KEY (judge_id) REFERENCES users(id)
);

-- competitors table
CREATE TABLE competitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nick TEXT,
    age INTEGER,
    origin TEXT,
    event TEXT NOT NULL,
    evaluators INTEGER DEFAULT 0,
    currentscore REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY (event) REFERENCES events(eventname)
);

-- logs table
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    enrolled INTEGER,
    scored REAL,
    created TEXT DEFAULT 'N/A',
    comment TEXT DEFAULT '',
    details TEXT DEFAULT '',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (enrolled) REFERENCES competitors(id),
    FOREIGN KEY (scored) REFERENCES competitors(currentscore),
    FOREIGN KEY (created) REFERENCES events(eventname)
);

##  Front end Web Design
Being this is a Web Application with Python backend, the user interface was designed using HTML, CSS, Bootstrap, JavaScript and Jinja Syntaxt.


Layout:
opted for a very simplistic design with black navbar ribbon on top with minimal buttons for Log in, Log out Registration and About page (more on those below). and at the bottom a transparent footer that holds social media and license information. Checkout the code for /layout.html in the templates file.


Index:
This is a simple landing page with one big button that starts the whole event creation process.
PS: users need to be logged into a session to access the index page. Checkout the code for /index.html in the templates file.

About:
The about page is designed with a column card layout and a header. It just holds some text that explains the general functionality of the tool. Checkout the code for /index.html in the templates file.

Register:
Allows for new users to create their account in order to judge. Has a common conventional form lay out to take in the user name, a password and the repeat the pass word before a button for singing on completes the form. Take a look at the code for /index.html in the templates file.

Login:
Simple User Name and Password from for user with existing accounts to log in, there’s also a tiny link that routs the user to register.html in the case they don’t have an account yet.

Create:
If an when users click on the big button on the index page, the event creation form appears. this form uses a card layout just for look and feel. First card asks for a title for the event. Second asks for date and sport/discipline the event is for. Third card (same form) asks for the amount of competitors and how many runs the event will hold(runs form is laid out in radio check boxes). Forth and final card of the form asks for Judge amount, Soring type and aggregation type. Judge count was made a little bit more dynamic through the use of some JavaScript, so that depending on how many judges are selected for the event, that many input boxes will appear on the form. the other 2 questions on the form are in drop down menu format, before the final submit button is available. after completion create directs the user directly to enroll.html.

Enroll:
After the event is created, depending on the competitors count selected on the previous form, enroll will produce a form with the same amount of input boxes for the amount of competitors for the event (this is handled in the back end). for each competitor there will be boxes for name, nick name, age and origin, of which only name and age are mandatory. once all contestants names have filled out the form, the submit button takes the user to the next page, succes.html.  You may take a look at the code for /enroll and /create in the templates file.

Success:
This page indicates to the user that an event has been successfully created. It is a simple in between screen, that holds information about the event. a button takes the user to where the actual scoring takes place, eventscore.html. Checkout the code for /success .html in the templates file.

Event score:
Will show a table per run, depending on the amount of runs selected for the contest. each table will have the name of the competitors enlisted and a number input box for the score .once each competitor has received a score for each of their runs, the user can submit scores which will bring them over to the final page, results.html

Results:
After scores have been submitted by the users, the final screen displays the results of the contests back to the user in a list container lay out. This list sorted by highest score and down and shows the standings as well (this again is handled by the backend)

##  Back end Logic:

####Route for the landing page:@app.route("/")
 - Landing page for the FAST app
  -Redirects logged-in users to the main index page.
  -Requires user authentication using a login_required decorator.
  -return render_template("index.html")

####Route for the about page @app.route("/about", methods=["GET"])
   -Renders the about page with details about the application.
   - returns render_template for ("about.html")

####Route for user registration@app.route("/register", methods=["GET", "POST"])
   - Handles user registration.
   - GET: Renders the registration form.
   - POST: Processes user registration, validating and storing new user data.
   - Redirects to the login page upon successful registration.
   - Displays flash messages for registration errors.

####Route for user login methods="GET", "POST"
 - Handles user login."""
  - GET: Renders the login form.
  - POST: Processes user login, validating credentials and establishing a user session.
  - Redirects to the main index page upon successful login.

####Route for event creation @app.route("/create", methods=["GET", "POST"])
#####This function is a Flask route decorated with **`@app.route("/create", methods=["POST", "GET"])`**, indicating it handles requests to the "/create" URL using both GET and POST methods.

-  Handles the creation of events.
-  GET: Renders the event creation form.
- Redirects to the enrollment page upon successful event creation.
- The **`@login_required`** decorator ensures that only authenticated users can access this route.
- The route checks if the request method is POST (indicating a form submission). If true, it retrieves form data using **`request.form.get()`**.
- The data obtained from the form is stored in the Flask session for later use during the enrollment process.
- checks if the provided judge names exist in the users table. If a judge name is not found, it flashes an error message and redirects to "/create".
- For each valid judge, it inserts event data into the events table

####Route for competitor enrollment @app.route("/enrollment", methods=["GET", "POST"])
  - Handles competitor enrollment for an event."""
  - This function is a Flask route decorated with @app.route("/enrollment", methods=["GET", "POST"]).
  - GET: Renders the competitor enrollment form.
  - POST: Processes the form data, enrolling competitors for an event.
  - It checks if the request method is POST (indicating a form submission) and retrieves form data using request.form.get().
  - Redirects to the success page upon successful enrollment.
  - The route processes competitor enrollment data (you would typically store this data in the database).

####Route for success page @app.route "/success", methods=["GET"]
   -GET: Renders the success page with details about the created event.

####Route for event scoring@app.route("/eventscore", methods=["GET", "POST"])
   -Handles event scoring."""
   - GET: Renders the event scoring form with competitor information. For a GET request, it retrieves relevant data (event details, competitor names) for rendering the event scoring form.
   - POST: Processes the submitted scores, updates competitor scores in the database. For a POST request, it would process the submitted scores, update the database, and redirect to the results page.
   -  Redirects to the event score page upon successful scoring.

####Route for displaying event results @app.route("/results", methods=["GET"])
    - GET: Retrieves competitor scores for an event, sorts and renders the results page.
    - Retrieves relevant data (event details, competitor names, scores) from the database.
    - Sorts the list of competitors based on their current scores in descending order.
    - Renders the "results.html" template with the sorted competitors data.

Side Note:
Originally this App was aimed for BMX competitions, but quickly it can be easy to see how several other AC related sports use a similar scoring system and can benefit from using such software .In that regard this program may also be used to keep score per say skate boarding competition

Non-technical Resources:

https://www.espn.com/gallery/11827867/the-afterlife-action-sports-industry-jobs
https://olympics.com/en/news/bmx-freestyle-world-cup-2023-schedule-scoring-format
https://www.w3schools.com/cssref/css_selectors.php
