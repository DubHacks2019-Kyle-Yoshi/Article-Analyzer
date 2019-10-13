from flask import Flask, request, render_template
import urllib.request
import requests as rq
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route('/handledata', methods=['POST'])
def handle_data():
    url = request.form['url']

    with urllib.request.urlopen(url) as fp:
        soup = BeautifulSoup(fp, "html.parser")
    text = soup.get_text()

    return render_template('show_results.html')


@app.route('/')
def index():
    return render_template('index.html')
