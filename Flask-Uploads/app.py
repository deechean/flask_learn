from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed, TEXT

app = Flask(__name__)

files = UploadSet("default", IMAGES+TEXT)
#photos = UploadSet("photos", IMAGES)
#docs = UploadSet("photos", TEXT)

# app.config["UPLOADED_PHOTOS_DEST"] = "pictures" # middle name must be the same as the name defined in UploadSet
# app.config["UPLOADED_PHOTO_ALLOW"] = ["jpg","bmp","tiff","txt"]
# app.config["UPLOADED_PHOTO_DENY"] = ["zip","exe"]

app.config["UPLOADED_DEFAULT_DEST"] = "uploaded"

#configure_uploads(app, photos)
configure_uploads(app, files)

@app.route("/uploads",methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "thefile" in request.files:
        try:
            image_filename = files.save(request.files["thefile"])
            return "<h1>"+files.url(image_filename)+"</h1>"
        except UploadNotAllowed:
            return "<h1>File is not allowed!</h1>"
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)