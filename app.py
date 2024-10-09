
from boltiotai import openai 
import os 
import sys 
from flask import Flask, render_template_string
from flask import Flask, request
from openai import OpenAI 
 #from .content_generator import generate_educational_content
#from . import generate_educational_content  # Add this import

# Set up the OpenAI API key try
try:
   
    openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
     sys.stderr.write("""You haven't set up your API key yet. If you don't have an API key yet, visit:https://platform.openai.com/signup
1.	Make an account or sign in
2.	Click "View API Keys" from the top right menu.
3.	Click "Create new secret key"
Then, open the Secrets Tool and add OPENAI_API_KEY as a secret.""") 
     exit(1)
def generate_lyrics_content(Create_Update_lyrics, Language, Genre):
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant"
        },
        {
            "role": "user",
            "content": ( f"Generate song lyrics in {Language} for a {Genre} song ."
                         "The lyrics should  follow: {Create_Update_lyrics}.\n"
                         "Make sure to keep the structure suitable for a song with verses, a chorus, and a bridge."
            )
        }
    ]
)
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Initialize Flask application app = Flask(__name__)
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    output = ""
    if request.method == 'POST':
        Create_Update_lyrics = request.form['Create_Update_lyrics']
        Language = request.form['Language']
        Genre = request.form['Genre']
        output = generate_lyrics_content(Create_Update_lyrics, Language, Genre)
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lyrics Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            color: #333;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 700px;
            margin-top: 50px;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: #007bff;
        }
        .form-label {
            font-weight: bold;
        }
        .btn-primary {
            background-color: #007bff;
            border-color: #007bff;
        }
        .btn-primary:hover {
            background-color: #0056b3;
            border-color: #0056b3;
        }
        .card {
            margin-top: 20px;
        }
        .card-header {
            background-color: #007bff;
            color: #fff;
            font-weight: bold;
        }
        .btn-secondary {
            background-color: #6c757d;
            border-color: #6c757d;
        }
        .btn-secondary:hover {
            background-color: #5a6268;
            border-color: #545b62;
        }
    </style>

    <script>
        async function generateContent() {
            const form = document.querySelector('#content-form');
            const output = document.querySelector('#output');
            const loading = document.querySelector('#loading');
            output.textContent = '';
            loading.style.display = 'block';

            const response = await fetch('/generate', {
                method: 'POST',
                body: new FormData(form)
            });

            const newOutput = await response.text();
            loading.style.display = 'none';
            output.innerHTML = newOutput;
        }

        function copyToClipboard() {
            const output = document.querySelector('#output');
            const textarea = document.createElement('textarea');
            textarea.value = output.textContent;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            alert('Copied to clipboard');
        }
    </script>
</head>
<body>
<div class="container">
    <h1 class="my-4"><strong>Lyrics Generator</strong></h1>
    <form id="content-form" onsubmit="event.preventDefault(); generateContent();" class="mb-3">
        <div class="mb-3">
            <label for="Language" class="form-label"><strong>Language:</strong></label>
            <input type="text" class="form-control" id="Language" name="Language" placeholder="Enter the language" required>

            <label for="Genre" class="form-label"><strong>Genre:</strong></label>
            <input type="text" class="form-control" id="Genre" name="Genre" placeholder="Enter the song genre" required>

            <label for="Create_Update_lyrics" class="form-label"><strong>Create/Update lyrics:</strong></label>
            <input type="text" class="form-control" id="Create_Update_lyrics" name="Create_Update_lyrics" placeholder="Enter the lyrics" required>
        </div>
        <button type="submit" class="btn btn-dark">Generate song lyrics</button>
    </form>
    <div id="loading" style="display:none;">Generating content, please wait...</div>
    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            <strong>Output:</strong>
            <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy</button>
        </div>
        <div class="card-body">
            <pre id="output" class="mb-0" style="white-space: pre-wrap;">{{ output }}</pre>
        </div>
    </div>
    <div class="alert alert-info mt-4" role="alert">
        <strong>Data Privacy Notice:</strong> Your input data is used only to generate content and is not stored or logged.
    </div>
</div>
</body>
</html>

''', output=output)
@app.route('/generate', methods=['POST']) 
def generate():
    Create_Update_lyrics = request.form['Create_Update_lyrics']
    Language = request.form['Language']
    Genre = request.form['Genre']
    content = generate_lyrics_content(Create_Update_lyrics,Language,Genre)

    return content
if __name__ == '__main__':
    app.run(debug=True)

