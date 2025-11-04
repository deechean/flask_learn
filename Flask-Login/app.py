from flask import Flask, render_template, request, get_flashed_messages, session, \
    redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, \
      logout_user, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse, urljoin
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

login_manager = LoginManager()

app = Flask(__name__)
app.config["SECRET_KEY"]="secret" #gen_random_key()
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlites3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager.init_app(app)

db = SQLAlchemy()
db.init_app(app)
serializer = URLSafeTimedSerializer(app.secret_key)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    session_token = db.Column(db.String(100), unique=True)

    def get_id(self):
        return str(self.session_token)

def create_user(username, password):
    user = User(username="deechean", password="password1", session_token=serializer.dumps(["deechean", "password1"]))
    db.session.add(user)
    db.session.commit()

def update_token(username, password):
    user = User.query.filter_by(username=username).first()
    user.password = password
    user.session_token = serializer.dumps([username, password])
    db.session.commit()

login_manager.login_view = "login"
login_manager.login_message = "You cannot access that page. You need to login first."
login_manager.refresh_view = "login"
login_manager.needs_refresh_message = "You need to login again."

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

@login_manager.user_loader
def load_user(session_token):
    user = User.query.filter_by(session_token=session_token).first()        
    try:
        serializer.loads(session_token, max_age=120)
    except SignatureExpired:
        user.session_token = None
        db.session.commit()
    return user


@app.route("/profile")   
@login_required 
def profile():
    return f"<h1>You are in the profile, {current_user.username}.</h1>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":        
        username = request.form.get("username")
        remember_me = request.form.get("remember_me")
        user = User.query.filter_by(username=username).first()

        if not user:
            return f"<h1>User does not exist!</h1>"   
        update_token(user.username, user.password)     
        
        #remember=True, when close browse, the session will be remembered
        login_user(user, remember=remember_me)         

        if "next" in session and session["next"]: 
            if is_safe_url(session["next"]):
                return redirect(session["next"])

        return redirect(url_for("index"))
    
    session["next"] = request.args.get("next")
    return render_template("login.html")

@app.route("/logout")
@login_required 
def logout():
    logout_user()
    return "<h1>You are now logged out!</h1>"

@app.route("/")
def index():
    return f"<h1>You are on home page.</h1>"  

@app.route("/change")
@fresh_login_required
def change():
    return "<h1>This is for fresh logins only!</h1>"
 

if __name__ == "__main__":    
    app.run(debug=True)
    
    #with app.app_context():
    #    create_user("deechean", "password1")
    #update_token("deechean", "password1")