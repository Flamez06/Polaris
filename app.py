from flask import Flask, render_template, request, redirect, url_for
import json, random

app = Flask(__name__)

# Define the path to the JSON file
DATABASE = 'data.json'
USERNAME = ''

# Load existing data from the JSON file
def load_data():
    try:
        with open(DATABASE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"users": {}, "tweets": []}
        with open(DATABASE, 'a')as f:
            json.dump(data, f)
    return data

# Save data to the JSON file
def save_data(data):
    with open(DATABASE, 'w') as file:
        json.dump(data, file, indent=4)

# used for assigin a random string to a post
def random_string():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(letters) for i in range(10))

# Home page - display all tweets
@app.route('/', methods=['GET', 'POST'])
def home():
    data = load_data()

    if request.method == 'POST':
        request_load = dict(request.form)

        if "tweet" in request_load:
            tweet = request_load['tweet']
            id = random_string()
            data['tweets'][id] = [USERNAME, tweet, data['users'][USERNAME][1], []]
            data['users'][USERNAME][2].append(id)
            
        if "like" in list(request_load.keys())[0]:
            id = list(request_load.keys())[0].split('-')[1]
            if USERNAME != '':
                if not USERNAME in data['tweets'][id][3]:
                    data['tweets'][id][3].append(USERNAME)
                else:
                    data['tweets'][id][3].remove(USERNAME)
        
        save_data(data)

    if not USERNAME == '':
        return render_template('index.html', tweet_keys=list(data['tweets'].keys())[::-1], tweets=list(data['tweets'].values())[::-1], user=USERNAME, pfp=data['users'][USERNAME][1])
    else:
        return render_template('index.html', tweet_keys=list(data['tweets'].keys())[::-1], tweets=list(data['tweets'].values())[::-1], user=USERNAME, pfp='')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = load_data()
        username = request.form['username']
        password = request.form['password']
        if username in data['users']:
            error = 'Username already taken'
            return render_template('register.html', error=error)
        data['users'][username] = [password,"../static/Images/default.png", []]
        save_data(data)
        return redirect(url_for('login'))
    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = load_data()
        global USERNAME
        USERNAME = request.form['username']
        password = request.form['password']
        if USERNAME not in data['users'] or data["users"][USERNAME][0] != password:
            error = 'Invalid credentials'
            return render_template('login.html', error=error)
        return redirect(url_for('home'))
    return render_template('login.html')

# User profile page - display user's tweets and allow posting new tweets
@app.route('/account', methods=['GET', 'POST'])
def account():
    try:
        data = load_data()
        user_tweets = data['users'][USERNAME][2]
        img=data['users'][USERNAME][1]
        tweets_collection = data['tweets']

        if request.method == 'POST':
            request_load = dict(request.form)

            if "like" in list(request_load.keys())[0]:
                id = list(request_load.keys())[0].split('-')[1]
                if USERNAME != '':
                    if not USERNAME in data['tweets'][id][3]:
                        data['tweets'][id][3].append(USERNAME)
                    else:
                        data['tweets'][id][3].remove(USERNAME)
            
            save_data(data)

        return render_template('profile.html', user=USERNAME, tweet_keys=data['users'][USERNAME][2] , tweets=user_tweets[::-1], data=tweets_collection, pfp=img)
    except:
        return render_template("error.html")
    

@app.route('/profile/<user>', methods=['GET', 'POST'])
def profile(user):
        data = load_data()
        user_tweets = data['users'][user][2]
        img=data['users'][user][1]
        tweets_collection = data['tweets']

        if request.method == 'POST':
            request_load = dict(request.form)

            if "like" in list(request_load.keys())[0]:
                id = list(request_load.keys())[0].split('-')[1]
                if USERNAME != '':
                    if not USERNAME in data['tweets'][id][3]:
                        data['tweets'][id][3].append(USERNAME)
                    else:
                        data['tweets'][id][3].remove(USERNAME)
            
            save_data(data)

        return render_template('profile.html', user=user, tweet_keys=data['users'][user][2] , tweets=user_tweets[::-1], data=tweets_collection, pfp=img)
   

if __name__ == '__main__':
    app.run(debug=True)
