import json 
from poseDetection import PoseDetectionAlgo
import cv2 


class CameraRead(): 

    def __init__(self, camera_path = "../data/youTube_video.mp4"): 
        self.camera = cv2.VideoCapture(camera_path)

    def update(self, updated_path): 
        self.camera = cv2.VideoCapture(updated_path)

    @property 
    def read(self): 
        return self.camera 
        

class PoseObj(): 
    def __init__(self): 
        self.counter = 0 
        self.pose = 0 
        self.pose_detection = PoseDetectionAlgo() 
    
    @property
    def RepCounter(self): 
        return self.counter   

    def RepCountWrite(self): 
        with open(".json", "w") as file: 
            json.dumps(file)

    def gen_frames(self, camera, pose):  # generate frame by frame from camera

        flag = True 
        run_once = 0
        while True:
            success, frame = camera.read() 
            if run_once == 0: 
                run_once = 1 
                self.pose_detection.SetRefferences(frame)
            if success:
                
                if(self.pose): 
                    if flag:
                        frame, self.counter, stage = self.pose_detection.pose_detection_mediapipe(frame, 0, None)
                        
                        flag = False 
                    else:
                        frame, self.counter, stage  = self.pose_detection.pose_detection_mediapipe(frame, self.counter, stage)
                        
                    
                try:
                    ret, buffer = cv2.imencode('.jpg', cv2.flip(cv2.flip(frame,-1), -1))
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except Exception as e:
                    print("10"*40)
                    print("Error Occured")
                    print("10"*40)
                    pass
                    
            else:
                pass

    
    




