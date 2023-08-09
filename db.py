import mysql.connector
import json
db=mysql.connector.connect(
     host="localhost",
    user="root",
    passwd="wwoorrlldD1",
    database="polaris"
)
cursor=db.cursor()

def tweets():
    message=[];hash=[]
    cursor.execute("SELECT message FROM tweets")
    result1=cursor.fetchall()[::-1]
    cursor.execute("SELECT hash FROM tweets")
    result2=cursor.fetchall()[::-1]
    for i in range(len(result1)):
        message.append(json.loads(result1[i][0]))
        hash.append(result2[i][0])
    return (message,hash)

def post(tweet,id,username):
    cursor.execute("SELECT tweets FROM users WHERE name=%s",(username, ))
    result=json.loads(cursor.fetchone()[0])
    result['list'].append(id)
    cursor.execute("UPDATE users SET tweets=%s WHERE name=%s",(json.dumps(result),username))
    new_message=json.dumps([username,tweet,[]])
    cursor.execute("INSERT INTO tweets(hash,message) VALUES(%s,%s)",(id,new_message))
    db.commit()

def login():
    cursor.execute("SELECT name FROM users")
    result1=cursor.fetchall()
    cursor.execute("SELECT pass FROM users")
    result2=cursor.fetchall()
    return dict(zip(result1,result2))

def register(username,passw):
    cursor.execute("INSERT INTO users(name,pass,tweets) VALUES(%s,%s,%s)",(username,passw,json.dumps({'list':[]})))
    db.commit()

def delete(id):
    cursor.execute("DELETE FROM tweets WHERE hash=%s",(id,))
    db.commit()

def like_data(id):
    cursor.execute("SELECT message FROM tweets WHERE hash=%s",(id,))
    result=cursor.fetchone()
    return json.loads(result[0])

def like(id,msg):
    cursor.execute("UPDATE tweets SET message=%s WHERE hash=%s",(json.dumps(msg),id,))
    db.commit()

