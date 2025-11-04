from flask import Flask
from flask_mail import Mail, Message


def create_app():
    app = Flask(__name__)

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = "deechean@gmail.com"
    app.config["MAIL_PASSWORD"] ="tldgnuwukcdpccxy"
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    #app.config["MAIL_DEFAULT_SENDER"] = ("Deechean", "deechean@gmail.com")
    app.config["MAIL_MAX_EMAILS"] = 20

    #app_password = tldg nuwu kcdp ccxy
    mail = Mail()
    mail.init_app(app)

    @app.route("/")
    def index():
        msg = Message("New message", 
                      sender=("Deechean", "deechean@gmail.com"),
                      recipients=["diqian0412@gmail.com"])
        #msg.add_recipient("di-qian.wang@hp.com")
        #msg.body = "This is a plaintext message!"
        #msg.html = "<b>This is an HTML message!</b>"
        msg.html = "<b>Please see the attachment.</b>"

        with app.open_resource("20240119.jpg") as jpg:
            msg.attach("20240119.jpg", "image/jepg", jpg.read())

        mail.send(msg)

        return "<h1>Sent!</h1>"
    

    @app.route("/bulk")
    def bulk():
        users = [{"name": "Deechean", "email": "diqian0412@gmail.com"}]

        with mail.connect() as conn:
            for user in users:
                msg = Message("Bulk", recipients=[user["email"]])
                msg.body = f"Hey {user['name']}"
                conn.send(msg)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)