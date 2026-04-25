from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "http://localhost:8000/upload/"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    jd_text=""
    filename=""
    if request.method == "POST":
        file = request.files["resume"]
        jd = request.form["job_description"]

        files = {"file": (file.filename, file.stream, file.mimetype)}
        data = {"job_description": jd}

        response = requests.post(API_URL, files=files, data=data)

        if response.status_code == 200:
            result = response.json()

    return render_template(
        "index.html",
        result=result,
        jd_text=jd_text,
        filename=filename
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)