from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer

db = SQLAlchemy()
app = Flask(__name__)

app.config["SECRET_KEY"]="secret"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlites3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#serializer = URLSafeSerializer(app.secret_key)
serializer = URLSafeTimedSerializer(app.secret_key)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    session_token = db.Column(db.String(100), unique=True)

    def get_id(self):
        return str(self.session_token)

def create_user():
    user = User(username="deechean", password="password1", session_token=serializer.dumps(["deechean", "password1"]))
    db.session.add(user)
    db.session.commit()

def update_token(username, password):
    user = User.query.filter_by(username=username).first()
    user.password = password
    user.session_token = serializer.dumps([username, password])
    db.session.commit()

if __name__ == "__main__": 
    db.init_app(app)   
    #with app.app_context():
    #    db.create_all()    
    #    create_user()
    update_token("deechean", "password1")
    #app.run(debug=True)