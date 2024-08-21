import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__, template_folder='templates')
app.secret_key = '555'  # Set a secret key for session management

# Load JSON data
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
    print("Data loaded successfully.")
except FileNotFoundError:
    print("data.json file not found.")
    data = {}
except json.JSONDecodeError:
    print("Error decoding JSON from data.json.")
    data = {}

# Serve the welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Redirect to index.html when clicking "Drocker"
@app.route('/drocker')
def drocker():
    return redirect(url_for('index'))

# Serve the main page (index.html)
@app.route('/index')
def index():
    return render_template('index.html')

# Route for the IAM login page
@app.route('/login_iam')
def login_iam():
    return render_template('login.html')

# Endpoint to handle user input
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip().lower()
    
    # Process user input based on loaded JSON data
    response_message = process_user_input(user_message)

    response = {'message': response_message}
    return jsonify(response)

def process_user_input(user_message):
    # Check for general comments
    general_comments = data.get('general_comments', {})
    if user_message in general_comments:
        return general_comments[user_message]

    # Check for IAM concepts
    iam_concepts = data.get('iam_concepts', {})
    response_message = iam_concepts.get(user_message)
    if response_message:
        return response_message

    # Check for matching roles
    companies = data.get('companies', [])
    for sector in companies:
        for role in sector['roles']:
            if user_message in role['role'].lower():
                return (
                    f"Sector: {sector['name']}\n"
                    f"Role: {role['role']}\n"
                    f"Description: {role['description']}\n"
                    f"Permissions: {', '.join(role['permissions'])}\n"
                    f"Compliance: {', '.join(role['compliance'].keys())}"
                )

    # Fallback response if no match found
    return "Sorry, I didn't understand that. Please ask about a specific role or IAM concept."

if __name__ == '__main__':
    app.run(debug=True)
