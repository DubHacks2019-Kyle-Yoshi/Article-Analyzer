from flask import Flask, request, render_template
import urllib.request
import requests as rq
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


app = Flask(__name__)


@app.route('/handledata', methods=['POST'])
def handle_data():
    url = request.form['url']

    with urllib.request.urlopen(url) as fp:
        html = fp.read()
    sent_str = get_sentiment(html.decode())

    return render_template('show_results.html', sentiment=sent_str)


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
    
