import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@socketio.on('connected')
def handle_connected(json, methods=['GET', 'POST']):
    print('[Event]: ',  str(json))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html')


@socketio.on('incoming-msg')
def on_message(data):
    """Broadcast messages"""
    msg = data["msg"]
    username = data["username"]
    #room = data["room"]
    # Set timestamp
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    socketio.emit('message', {"username": username, "msg": msg, "time_stamp": time_stamp})
    #send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)

@app.route('/')
def sessions():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
