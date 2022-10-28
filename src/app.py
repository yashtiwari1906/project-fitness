from typing import Counter
from flask import Flask, render_template, Response, request, jsonify
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread, Event
from poseDetection import pose_detection_mediapipe

from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep



global global_counter, capture,rec_frame, grey, switch, neg, face, rec, out, pose, data, prev
global_counter = 0 
data = {"reps": 0}
prev = 0
capture=0
grey=0
neg=0
face=0
switch=1
rec=0
pose = 0
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



camera = cv2.VideoCapture("./data/youTube_video.mp4")
    
def pose_detection(frame, flag, y_hip_ref, y_knee_ref, counter, stage): 
    
    if flag:
        im, y_hip_ref, y_knee_ref, counter, stage = pose_detection_mediapipe(frame, flag, 0, 0, 0, None)
        data["reps"] = counter
        return im, y_hip_ref, y_knee_ref, counter, stage
    else:
        
        im, y_hip_ref, y_knee_ref, counter, stage = pose_detection_mediapipe(frame, flag, y_hip_ref, y_knee_ref, counter, stage)
        data["reps"] = counter
        return im, y_hip_ref, y_knee_ref, counter, stage

    
def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    flag = True 
    while True:
        success, frame = camera.read() 
        
        if success:
            
            if(pose): 
                if flag:
                    frame, y_hip_ref, y_knee_ref, counter, stage = pose_detection(frame, True, 0, 0, 0, None)
                    data["reps"] = counter
                    flag = False 
                else:
                    frame, y_hip_ref, y_knee_ref, counter, stage  = pose_detection(frame, False, y_hip_ref, y_knee_ref, counter, stage)
                    data["reps"] = counter
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(cv2.flip(frame,-1), -1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


@app.route('/')
def index():
    #print(f"index global counter {global_counter}")
    return render_template('index.html')
    
    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('pose') == 'pose detection': 
            global pose 
            pose = not pose 
            if pose: 
                time.sleep(4)
          
    elif request.method=='GET':
        
        return render_template('index.html')
    
    

    return render_template('index.html')

def reps_counter(): 
    global prev, data
    if data['reps']!=prev: 
        prev = data['reps'] 
        
    socketio.emit('newnumber', data, namespace='/test')



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
    socketio.run(app, port = 8000, host = "0.0.0.0")
camera.release()
cv2.destroyAllWindows()     
