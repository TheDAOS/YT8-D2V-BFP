from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    video_id = str(uuid.uuid4())
    filename = f"{video_id}.mp4"

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': filename
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    response = send_file(filename, as_attachment=True)
    os.remove(filename)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
