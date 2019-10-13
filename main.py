from flask import Flask, request, render_template
import urllib.request
import requests as rq
#from bs4 import BeautifulSoup
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


app = Flask(__name__)


@app.route('/handledata', methods=['POST'])
def handle_data():
    url = request.form['url']

    with urllib.request.urlopen(url) as fp:
        html = fp.read()
#        soup = BeautifulSoup(fp, "html.parser")
#    text = soup.get_text()
    get_sentiment(html.decode())

    return render_template('show_results.html')


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
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    
    #print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

