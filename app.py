from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Define the path to the JSON file
DATABASE = 'data.json'

# Load existing data from the JSON file
def load_data():
    try:
        with open(DATABASE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'users': {}, 'tweets': []}
    return data

# Save data to the JSON file
def save_data(data):
    with open(DATABASE, 'w') as file:
        json.dump(data, file)

# Home page - display all tweets
@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', tweets=data['tweets'])

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = load_data()
        username = request.form['username']
        if username in data['users']:
            error = 'Username already taken'
            return render_template('register.html', error=error)
        data['users'][username] = []
        save_data(data)
        return redirect(url_for('login'))
    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = load_data()
        username = request.form['username']
        if username not in data['users']:
            error = 'Invalid username'
            return render_template('login.html', error=error)
        return redirect(url_for('profile', username=username))
    return render_template('login.html')

# User profile page - display user's tweets and allow posting new tweets
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    data = load_data()
    user_tweets = data['users'].get(username, [])
    if request.method == 'POST':
        tweet = request.form['tweet']
        data['tweets'].append({'username': username, 'tweet': tweet})
        user_tweets.append({'tweet': tweet})
        save_data(data)
    return render_template('profile.html', username=username, tweets=user_tweets)

if __name__ == '__main__':
    app.run(debug=True)