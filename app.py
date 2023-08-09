from flask import Flask, render_template, request, redirect, url_for,jsonify,session
import json, random
from datetime import timedelta
import db

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
     tweet=request.form['tweet']
     USERNAME=session["user"]
     id = random_string()
     print(tweet,id,USERNAME)
     db.post(tweet,id,USERNAME)
     return redirect(url_for('home'))

# Home page - display all tweetscl
@app.route('/', methods=['GET', 'POST'])
def home():
    data=db.tweets()
    if request.method == 'POST':
        id = request.form['id']
        USERNAME=session["user"]
        ldata=db.like_data(id)
        if USERNAME not in ldata[2]:ldata[2].append(USERNAME)
        else:ldata[2].remove(USERNAME)
        db.like(id,ldata)
        return jsonify({'count':len(ldata[2])})

    if "user" in session:
        USERNAME=session["user"]
        return render_template('index1.html', tweet_keys=data[1], tweets=data[0],user=USERNAME)
    else:
        return render_template('index1.html', tweet_keys=data[1],tweets=data[0])

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = db.login()
        username = request.form['username']
        password = request.form['password']
        if (username, ) in data:
            error = 'Username already taken'
            return render_template('register.html', error=error)
        db.register(username,password)
        return redirect(url_for('login'))
    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' not in session:
        if request.method == 'POST':
            data = db.login()
            USERNAME = request.form['username']
            password = request.form['password']
            if (USERNAME, ) not in data or data[(USERNAME, )][0] != password:
                error = 'Invalid credentials'
                return render_template('login.html', error=error)
            try :
                check=request.form['rem']
                if check=="remember":
                    session.permanent=True
                    session["user"]=USERNAME
            except:
                session["user"]=USERNAME
            return redirect(url_for('home'))
        return render_template('login.html')
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
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
    
    return render_template('landing1.html') 


@app.route('/delete',methods=['POST'])
def delete():
        id=request.form['delmsg']
        db.delete(id)
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
