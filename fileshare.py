from flask import Flask, request, send_from_directory, render_template_string
import os
import qrcode

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
QR_FOLDER = "qr_codes"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>File Upload System</title>
    <style>
        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            text-align: center;
        }
        h1 {
            margin-top: 20px;
        }
        .box {
            background: #1e293b;
            padding: 20px;
            border-radius: 10px;
            width: 50%;
            margin: auto;
        }
        input[type=file] {
            margin: 10px;
        }
        button {
            background: #22c55e;
            border: none;
            padding: 10px 20px;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #16a34a;
        }
        .file {
            background: #334155;
            margin: 10px;
            padding: 10px;
            border-radius: 8px;
        }
        img {
            margin-top: 10px;
        }
    </style>
</head>
<body>

<h1>🚀 File Upload System</h1>

<div class="box">
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <br>
        <button type="submit">Upload</button>
    </form>
</div>

<h2>📂 Uploaded Files</h2>

{% for file in files %}
<div class="file">
    <p>{{ file }}</p>

    <a href="/download/{{ file }}">
        <button>Download</button>
    </a>

    <br>
    <img src="/qr/{{ file }}" width="120">
</div>
{% endfor %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Generate QR
            file_url = request.host_url + "download/" + file.filename
            qr = qrcode.make(file_url)
            qr.save(os.path.join(QR_FOLDER, file.filename + ".png"))

    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML, files=files)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/qr/<filename>")
def qr_code(filename):
    return send_from_directory(QR_FOLDER, filename + ".png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
