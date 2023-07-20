import os
from peewee import *
import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from app.information import info
from playhouse.shortcuts import model_to_dict
import re

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), user=os.getenv( "MYSQL_USER"),password=os.getenv("MYSQL_PASSWORD"), host=os.getenv("MYSQL_HOST"), port=3306)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField( default=datetime. datetime. now)

    class Meta:
        database = mydb
    
mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']

    if name == "":
        return "Invalid name", 400
    if content == "":
        return "Invalid content", 400
    if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
        return "Invalid email", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return { 
            'timeline_posts': [
                model_to_dict(p)
                for p in
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", name = info['name'], location = info['location'], url=os.getenv("URL"))

@app.route("/hobbies")
def hobbies():
    return render_template('hobbies.html', url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    timeline_posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.
    created_at.desc())]
    return render_template('timeline.html', title="Timeline", posts= timeline_posts)
