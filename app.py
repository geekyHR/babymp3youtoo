from flask import Flask, request, send_file, render_template_string
import os
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>BabyMP3YouToo</title>
    <style>
        body {
            background-color: white;
            font-family: sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        input, select, button {
            padding: 10px;
            font-size: 1em;
            margin: 5px;
            width: 80%;
            max-width: 500px;
        }
        #disclaimer {
            position: fixed;
            bottom: 10px;
            right: 10px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <form method="POST" action="/convert">
        <input type="text" name="url" id="url" placeholder="Paste your link here!" required><br>
        <select name="quality" required>
            <option value="64">Low (64 kbps)</option>
            <option value="128" selected>Medium (128 kbps)</option>
            <option value="320">High (320 kbps)</option>
        </select><br>
        <input type="text" name="filename" placeholder="Save as (without .mp3)" required><br>
        <button type="submit">Download Now</button>
    </form>

    <div id="disclaimer">
        <a href="#" onclick="alert('This tool is intended only for personal use by Kiran Baby Joseph.')">ⓘ Disclaimer</a>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", () => {
            const input = document.getElementById("url");
            navigator.clipboard.readText().then(text => {
                if (text.includes("youtube.com")) input.value = text;
            });
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form['url']
    quality = request.form['quality']
    filename = request.form['filename']
    output_filename = f"{filename}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'cookiefile': 'youtube_cookies.txt',  # 🧠 Required to bypass YouTube blocks
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        os.rename("temp.mp3", output_filename)
        return send_file(output_filename, as_attachment=True)
    except Exception as e:
        return f"<h3>❌ Error: {str(e)}</h3>"
    finally:
        if os.path.exists(output_filename):
            os.remove(output_filename)

# ✅ This part ensures it works on Render.com (dynamic ports)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
