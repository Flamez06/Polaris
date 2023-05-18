from flask import Flask, render_template, request, redirect, url_for,jsonify,session
import json, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key="hehfbiwdqnsci"
app.permanent_session_lifetime=timedelta(hours=720)

# Define the path to the JSON file
DATABASE = 'data.json'

# Load existing data from the JSON file
def load_data():
    try:
        with open(DATABASE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"users": {}, "tweets": {}}
        with open(DATABASE, 'a')as f:
            json.dump(data, f)
    return data

# Save data to the JSON file
def karma(likes):
    return likes*20

def save_data(data):
    with open(DATABASE, 'w') as file:
        json.dump(data, file, indent=4)

# used for assigin a random string to a post
def random_string():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(letters) for i in range(10))



@app.route('/post',methods=['POST'])
def post():
     data=load_data()
     request_load=request.form
     USERNAME=session["user"]
     tweet = request_load['tweet']
     id = random_string()
     data['tweets'][id] = [USERNAME, tweet, data['users'][USERNAME][1], []]
     data['users'][USERNAME][2].append(id)
     save_data(data)
     return redirect(url_for('home'))


# Home page - display all tweets
@app.route('/', methods=['GET', 'POST'])
def home():
    data = load_data()
    if request.method == 'POST':
        id = request.form['id']
        USERNAME=session["user"]
        if not USERNAME in data['tweets'][id][3]:
            data['tweets'][id][3].append(USERNAME)
        else:
            data['tweets'][id][3].remove(USERNAME)
        
        save_data(data)
        return jsonify({ 'count':len(data['tweets'][id][3])  })

    if "user" in session:
        USERNAME=session["user"]
        return render_template('index.html', tweet_keys=list(data['tweets'].keys())[::-1], tweets=list(data['tweets'].values())[::-1],user=USERNAME, pfp=data['users'][USERNAME][1])
    else:
        return render_template('index.html', tweet_keys=list(data['tweets'].keys())[::-1], tweets=list(data['tweets'].values())[::-1])

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
    if 'user' not in session:
        if request.method == 'POST':
            data = load_data()
            USERNAME = request.form['username']
            password = request.form['password']
            if USERNAME not in data['users'] or data["users"][USERNAME][0] != password:
                error = 'Invalid credentials'
                return render_template('login.html', error=error)
            session.permanent=True
            session["user"]=USERNAME
            return redirect(url_for('home'))
        return render_template('login.html')
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for('home'))

# User profile page - display user's tweets and allow posting new tweets
@app.route('/account', methods=['GET', 'POST'])
def account():
    try:
        USERNAME=session['user']
        data = load_data()
        user_tweets = data['users'][USERNAME][2]
        img=data['users'][USERNAME][1]
        tweets_collection = data['tweets']
        messages=data['users'][USERNAME][2]
        likes=0
        for i in messages:
            likes+=len(data['tweets'][i][3])
        return render_template('account.html', user=USERNAME, tweet_keys=data['users'][USERNAME][2] , tweets=user_tweets[::-1], data=tweets_collection, pfp=img,karma=karma(likes))
    except:
        return render_template("error.html")
 
@app.route('/landing')
def landing():
    return render_template('landing.html')


@app.route('/delete',methods=['POST'])
def delete():
        USERNAME=session['user']
        d=list((request.form).keys())[0]
        x=d.split()[1]
        d=d.split()[0]
        data=load_data()
        del data['tweets'][d]
        data['users'][USERNAME][2].remove(d)
        save_data(data)
        if x=="prof":
            return redirect(url_for('account'))
        else:
            return redirect(url_for('home'))

@app.route('/profile/<user>', methods=['GET', 'POST'])
def profile(user):
        data = load_data()
        user_tweets = data['users'][user][2]
        img=data['users'][user][1]
        tweets_collection = data['tweets']
        messages=data['users'][user][2]
        likes=0
        for i in messages:
            likes+=len(data['tweets'][i][3])
        return render_template('profile.html', user=user, tweet_keys=data['users'][user][2] , tweets=user_tweets[::-1], data=tweets_collection, pfp=img,karma=karma(likes))
   
if __name__ == '__main__':
    app.run(debug=True)
