from typing import Counter
from flask import Flask, render_template, Response, request, jsonify
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread, Event
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep              
from werkzeug.utils import secure_filename     
from utilities import PoseObj, CameraRead



#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')
app.config['SECRET_KEY'] = 'secret!'
#app.config['DEBUG'] = True
app.config["port"] = 8080 
app.config["host"] = '0.0.0.0'

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()
pose_func = PoseObj()


VideoFeed = CameraRead()


@app.route('/')
def index():
    #print(f"index global counter {global_counter}")
    return render_template('index.html')
    
    
@app.route('/video_feed')
def video_feed():
    global counter 
    return_feed = pose_func.gen_frames(VideoFeed.read, pose_func.pose)
    return Response(return_feed, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    if request.method == 'POST':
        if request.form.get('pose') == 'pose detection': 
            pose_func.pose = not pose_func.pose 
            if pose_func.pose: 
                time.sleep(4)
          
    elif request.method=='GET':
        
        return render_template('index.html')
    
    return render_template('index.html')

@app.route('/upload')
def upload(): 
    return render_template('upload.html', template_folder = "templates")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   global camera 
   if request.method == 'POST':
      f = request.files['file']
    
      f.save(os.path.join("../data/", secure_filename(f.filename)))
      VideoFeed.update(os.path.join("../data/", secure_filename(f.filename)))
      return render_template("index.html")

def reps_counter(): 
    while not thread_stop_event.isSet():

        socketio.emit('reps', pose_func.RepCounter, namespace='/test')
        socketio.sleep(2)



@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.is_alive():
        print("Starting Thread")
    thread = socketio.start_background_task(reps_counter)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, port = 5000, host = "0.0.0.0")
    VideoFeed.read.release()
    cv2.destroyAllWindows()     
