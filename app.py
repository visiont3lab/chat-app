import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, join_room, leave_room, send
import cv2
import base64
import io
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

rooms = ["lesson","entertainment","news"]

@socketio.on('connected')
def handle_connected(json, methods=['GET', 'POST']):
    #print("Risultati: ", json["data"]["m"])
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
    room = data["room"]
    # Set timestamp
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    #socketio.emit('message', {"username": username, "msg": msg, "time_stamp": time_stamp})
    #socketio.emit('message', {"msg": msg, "time_stamp": time_stamp})  
    send({"username": username, "msg": msg, "image": "", "time_stamp": time_stamp}, room=room)

@app.route('/',methods=['GET'])
def sessions():
    return render_template('index.html', rooms=rooms)

@socketio.on('join')
def on_join(data):
    """User joins a room"""
    username = data["username"]
    room = data["room"]
    for r in rooms:
        if r==room:
            join_room(r)
            time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
            msg =  username + " has joined the " + r + " room."
            send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=r)
        else:
            leave_room(r)
            time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
            msg =  username + " has left the " + r + " room."
            send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=r)

@socketio.on('leave')
def on_leave(data):
    """User leaves a room"""
    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room)


@socketio.on('image-processing')
def on_image(data):
    data_url = data["image"]
    room = data["room"]
    username = data["username"]
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    #socketio.emit('message', {"username": username, "msg": msg, "time_stamp": time_stamp})
    #socketio.emit('message', {"msg": msg, "time_stamp": time_stamp})  

    base64_img = data_url.replace('data:image/png;base64,','')
    base64_img_bytes = base64_img.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)

    # save incoming image
    with open('test.png', 'wb') as file_to_save:
        file_to_save.write(decoded_image_data)

    # Opencv
    nparr = np.fromstring(decoded_image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1



    # -------------------------------------------------------
    # Algoritm
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)





    # -------------------------------------------------------
    cv2.imwrite("img.png",img)
    image = open('img.png', 'rb')
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read)
    image_64_decode = base64.decodestring(image_64_encode) 
    #img_uri = "data:image/png;base64," + base64.b64encode(img).decode('utf-8') 
    #img_uri =  base64.b64encode(img)
    send({"username": username, "msg": "",  "image": image_64_decode, "time_stamp": time_stamp}, room=room)


if __name__ == "__main__":
    app.run(debug=True)
