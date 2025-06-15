from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return open("index.html").read()

@app.route("/convert", methods=["POST"])
def convert():
    url = request.form["url"]
    quality = request.form.get("quality", "192")
    user_filename = request.form.get("filename", "output").strip()
    safe_filename = "".join(c for c in user_filename if c.isalnum() or c in (' ', '_', '-')).rstrip()
    output_filename = f"{safe_filename}.mp3"

    if os.path.exists(output_filename):
        os.remove(output_filename)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        os.rename("temp.mp3", output_filename)
        return send_file(output_filename, as_attachment=True)
    except Exception as e:
        return f"<h3>❌ Error: {str(e)}</h3>"
if __name__ == "__main__":
    app.run(debug=True)
