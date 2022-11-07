# dictionary-api-python-flask/app.py
from flask import Flask, request, jsonify, render_template
from model.dbHandler import match_exact, match_like

app = Flask(__name__)


@app.get("/")
def index():
    """
    DEFAULT ROUTE
    This method will
    1. Provide usage instructions formatted as JSON
    """
    # response = {"usage": "/dict?=<word>"}
    # Since this is a website with front-end, we don't need to send the usage instructions
    response = { 'usage': '/dict?=<word>' }
    return render_template("search.html")


@app.get("/dict")
def dictionary():
    """
    DEFAULT ROUTE
    This method will
    1. Accept a word from the request
    2. Try to find an exact match, and return it if found
    3. If not found, find all approximate matches and return
    """
    words = request.args.getlist("word") #get multiple parameters
    results = { 'words': [] }

    if not words:
        return jsonify({ "data": 'invalid word or no word provided' })

    for word in words:    
        definition = match_exact(word)
        if definition:
            results['words'].append({ 'status': 'success', 'word': word, 'data': definition })
        else:
            definitions = match_like(word) # try an approximate math
            if definitions:
                results['words'].append({ 'status': 'partial', 'word': word, 'data': definitions})

            else:
                results['words'].append({ 'status': 'error' , 'data': 'word no found'})
    
    #return jsonify(results)
    return render_template("results.html", response = jsonify(results))

if __name__ == "__main__":
    app.run()
