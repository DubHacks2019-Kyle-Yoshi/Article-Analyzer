from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/handledata', methods=['POST'])
def handle_data():
    url = request.form['url']
    print(" ")
    print("The string you entered was:", url)
    print(" ")
    return "this is where we will give the analysis of the text :)"

@app.route('/')
def index():
    return render_template('index.html')
