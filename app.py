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
        data = {"users": {},"tweets": []}
        with open(DATABASE,'a')as f:
            json.dump(data,f)
    return data

# Save data to the JSON file
def save_data(data):
    with open(DATABASE, 'w') as file:
        json.dump(data, file, indent=4)

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
        password=request.form['password']
        if username in data['users']:
            error = 'Username already taken'
            return render_template('register.html', error=error)
        data['users'][username] = [password]
        save_data(data)
        return redirect(url_for('login'))
    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = load_data()
        global username
        username = request.form['username']
        password=request.form['password']
        if username not in data['users'] or data["users"][username][0]!=password:
            error = 'Invalid credentials'
            return render_template('login.html', error=error)
        return redirect(url_for('profile', username=username))
    return render_template('login.html')

# User profile page - display user's tweets and allow posting new tweets
@app.route('/profile', methods=['GET', 'POST'])
def profile():
   try: 
        data = load_data()
        user_tweets = data['users'][username][1:]
        if request.method == 'POST':
            tweet = request.form['tweet']
            data['tweets'].append([username,tweet])
            data['users'][username].append(tweet)
            save_data(data)
        return render_template('profile.html', username=username, tweets=user_tweets)
   except:
       return "ACCESS DENIED. PLEASE LOGIN TO REACH THIS PAGE."

if __name__ == '__main__':
    app.run(debug=True)