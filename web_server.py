#!/usr/bin/env python
__author__ = 'giladfride'

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from urllib import urlopen, urlretrieve
import re
import mysocket
import disp_defines
import os

# The secret file is not included in the git repo since it contains private stuff.
# File should contain:
# camera_snapshot_url - a URL to a webcam JPG snapshot
try:
    import secret
except ImportError:
    print "Error - secret.py file is missing."

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def main_menu():
    return render_template("default.html")

@app.route('/send_msg')
def send_msg():
    return render_template('send_msg.html')

@app.route('/send_msg_post', methods=['POST'])
def send_msg_post():
    display_msg(request.form['msg_text'])
    flash('Message sent')
    return redirect(url_for('main_menu'))

@app.route('/camera1')
def camera_view():
    urlretrieve(secret.camera_snapshot_url,"static/snap1.jpg")
    return render_template("camera.html")


def get_ip_addr():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

def display_msg(msg):
    send_op("disp_msg(\"" + msg + "\")")

def send_op(op):
    soc = mysocket.MySocket()
    soc.connect("127.0.0.1", disp_defines.DISP_SERVER_PORT)
    soc.mysend(op)
    soc.close()


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')
    #app.run()
    #display_msg("adasd")