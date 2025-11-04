from flask import Flask, request, render_template, flash
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed, TEXT

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

video = UploadSet("video", ("mp4"))
app.config["UPLOADED_VIDEO_DEST"] = "video" 
configure_uploads(app, video)

@app.route("/uploads",methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "thefile" in request.files:
        try:
            filename = video.save(request.files["thefile"])
            flash("Upload completed!", "success")
        except UploadNotAllowed:
            return "<h1>File is not allowed!</h1>"
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)


