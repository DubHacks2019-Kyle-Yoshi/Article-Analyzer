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

    # Check if http in from of url or not
    if url[:4] != "http":
        url = "https://" + url

    with urllib.request.urlopen(url) as fp:
        html = fp.read()
    try:
        sent_str = get_sentiment(html.decode())
    except:
        return """
        Sorry, this URL cannot be processed
        <br />
        <a href="/">Go Back</a>
    """
    str_to_template = [round(sent_str.magnitude * sent_str.score, 2), round(sent_str.score, 2), '']

    if str_to_template[1] < -.14:
        str_to_template[2] = frowny
    elif str_to_template[1] > .14:
        str_to_template[2] = smiley
    else:
        str_to_template[2] = meh

    return render_template('show_results.html', sentiment=str_to_template)


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
    return client.analyze_sentiment(document=document).document_sentiment
    
