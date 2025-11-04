from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlites3" 
app.config["SECRET_KEY"] = "mysecret" 


db = SQLAlchemy(app)
admin = Admin(app, template_mode="bootstrap3")

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    age= db.Column(db.Integer)
    birthday = db.Column(db.DateTime)
    #session_token = db.Column(db.String(100), unique=True)
    comments = db.relationship("Comment", backref="user" , lazy="dynamic")

    def __repr__(self):
        return "<User %r>"%(self.username)

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Comment %r>"%(self.id)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))

if __name__ == "__main__":    
    app.run(debug=True)
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all() 
