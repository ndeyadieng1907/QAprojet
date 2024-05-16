from flask import Flask, render_template, request, jsonify
from my_QA_app import repondre
app = Flask(__name__)

# Define a route to render the form
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    query = request.form['query']
    answer, réponse = repondre(question=query)
    #email = request.form['email']
    
    # Process the form data (you can perform any operations here)
    #result = f"Résultat de la recherche : \n\n {réponse}"

    # Render a template with the result
    return render_template('index.html', answer = answer, result=réponse)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
