from flask import Flask, request, render_template
import urllib.request
import requests as rq
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


app = Flask(__name__)


smiley = "smile"
frowny = "frown"
meh = "meh"


@app.route('/handledata', methods=['POST'])
def handle_data():
    url = request.form['url']

    if len(url) < 5:
        return """
            Sorry, this URL cannot be processed
            <br />
            <a href="/">Go Back</a>
        """

    # Check if http in from of url or not
    if url[:4] != "http":
        url = "https://" + url

    with urllib.request.urlopen(url) as fp:
        html = fp.read()
    try:
        language_data = get_sentiment(html.decode())
    except:
        return """
        Sorry, this URL cannot be processed
        <br />
        <a href="/">Go Back</a>
    """


    face = ""
    if language_data.document_sentiment.score < -.14:
        face = frowny
    elif language_data.document_sentiment.score > .14:
        face = smiley
    else:
        face = meh

    score = language_data.document_sentiment.score * language_data.document_sentiment.magnitude
    return render_template('show_results.html', score=score, sent=language_data.document_dentiment.score, face=face)


@app.route('/')
def index():
    return render_template('index.html')


def get_sentiment(html):
    # Instantiates a client
    client = language.LanguageServiceClient()
    
    # The text to analyze
    #text = u'Hello, world!'
    document = types.Document(
        content=html,
        type=enums.Document.Type.HTML)
    
    # Detects the sentiment of the text
    return client.annotate_text(document=document)
    
