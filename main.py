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


def failed():
    return """
            Sorry, this URL cannot be processed
            <br />
            <a class="back" href="/">Go Back</a>
        """


@app.route('/handledata', methods=['POST'])
def handle_data():
    url = request.form['url']

    if len(url) < 5:
        return failed()

    # Check if http in from of url or not
    if url[:4] != "http":
        url = "https://" + url

    with urllib.request.urlopen(url) as fp:
        html = fp.read().decode()
    try:
        sent_str = get_sentiment(html)
    except:
        return failed()

    try:
        classification = get_classification(html)
    except:
        return failed()

    try:
        entities = get_entity(html)
    except:
        print("here")
        return failed()

    str_to_template = [round(sent_str.magnitude * sent_str.score, 4), round(sent_str.score, 3), '']

    bgcolor = "#f9f1f1"
    if str_to_template[1] < -.14:
        str_to_template[2] = frowny
        bgcolor = "lightred"
    elif str_to_template[1] > .14:
        str_to_template[2] = smiley
        bgcolor = "lightgreen"
    else:
        str_to_template[2] = meh
        bgcolor = "lightgrey"

    return render_template('show_results.html', sentiment=str_to_template, class_list=classification, bgcolor=bgcolor, entity_list=entities)


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
    
def get_classification(html):
    client = language.LanguageServiceClient()

    document = types.Document(
        content=html,
        type=enums.Document.Type.HTML)

    return client.classify_text(document=document).categories
    
def get_entity(html):
    client = language.LanguageServiceClient()

    document = types.Document(
        content=html,
        type=enums.Document.Type.HTML)

    return client.analyze_entity_sentiment(document=document).entities
    
