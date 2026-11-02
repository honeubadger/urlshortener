import random
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

links = {} #TODO: Implement database storage for links instead of using a dictionary

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" #TODO: Create an environment variable for the characters used in the random path generation

@app.route('/')
def home():
    homepage = open("./webpages/home.html", 'r') #Had to read the file everytime home is called
    table = ""
    for k in links:
        table += f"<tr><td>{list(links.keys()).index(k) + 1}</td><td>{"domain.com/" + k}</td><td>{links[k]}</td></tr>"
    return render_template_string(homepage.read(), history=table)

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        path = request.form.get('custom')
        link = request.form.get('url')
        if path and link:
            links[path] = link
            return redirect('/')
        elif link:
            random_path = ''.join(random.choice(chars) for _ in range(5))
            links[random_path] = link
            return redirect('/')
        else:
            return "Please provide a URL to shorten.", 400

@app.route('/<path>')
def dynamic_route(path):
    try:
        link = links[path]
        return redirect(link)
    except KeyError:
        return f"No link found for path: {path}", 404