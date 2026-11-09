import os
import random
from flask import Flask, redirect, render_template_string, request
import flask, urllib.parse
import database

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" #TODO: Create an environment variable for the characters used in the random path generation

def init_user():
    flask.session['user'] = "anonymous" #TODO: Implement user authentication and session management

@app.route('/')
def home():
    init_user()
    homepage = open("./webpages/home.html", 'r') #Had to read the file everytime home is called
    table = ""
    database.cursor.execute("SELECT * FROM links") # Fetch all links from the database
    links = database.cursor.fetchall() # Fetch all links from the database
    domain = "http://" + str(urllib.parse.urlparse(flask.request.base_url).hostname)
    for k in links:
        #table += f"<tr><td>{list(links.keys()).index(k) + 1}</td><td>{"domain.com/" + k}</td><td>{links[k]}</td></tr>"
        table += f"<tr><td>{k[0]}</td><td><a href={k[1]}>{k[1]}</a></td> \
            <td><a href={domain + ":5000/" + k[2]}>{domain + "/" + k[2]}</a></td></tr>" #added port number for development
    return render_template_string(homepage.read(), history=table)

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        path = request.form.get('custom')
        link = request.form.get('url')
        if path and link:
            database.add_link(link, path)
            return redirect('/')
        elif link:
            random_path = ''.join(random.choice(chars) for _ in range(5))
            database.add_link(link, random_path)
            return redirect('/')
        else:
            return "Please provide a URL to shorten.", 400

@app.route('/<path>')
def dynamic_route(path):
    try:
        database.cursor.execute("SELECT url FROM links WHERE path = %s", (path,))
        link = database.cursor.fetchone()
        if link:
            return redirect(link[0])
        else:
            return f"No link found for path: {path}", 404
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"An error occurred while processing your request: {e}", 500