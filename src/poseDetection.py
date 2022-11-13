
import cv2
from cv2 import destroyAllWindows
import mediapipe as mp
import numpy as np



class PoseDetectionAlgo(): 
    def __init__(self): 
        self.flag = True 
        self.y_hip_ref, self.y_knee_ref = 0, 0 
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose
        pass 

    def SetRefferences(self, frame):
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            
        
            if frame is not None:
                frame_ = self.rescale_frame(frame, percent=75)
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
            height, width, d = image.shape
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
        
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            
            # Get coordinates
            hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            #print("flag is {}".format(flag))
            
            self.y_hip_ref = hip[1]*height + hip[1]*(8/100)*height
            self.y_knee_ref = knee[1]*height - knee[1]*(8/100)*height   
        


    def calculate_angle(self, a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle


    def rescale_frame(self, frame, percent=50):
        width = int(frame.shape[1] * percent/ 100)
        height = int(frame.shape[0] * percent/ 100)
        dim = (width, height)
        try:
            return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)
        except:
            print("frame was empty!!!") 
            return frame

    # Youtube video

    def pose_detection_mediapipe(self, frame, counter, stage):
        angle_min = []
        angle_min_hip = []
        

        # Curl counter variables
        
        min_ang = 0
        max_ang = 0
        min_ang_hip = 0
        max_ang_hip = 0
        

        width, height = frame.shape[:2]
        size = (640, 480)
        #print("reached till here!!")
        #fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        #out = cv2.VideoWriter('output_video_.avi', fourcc, 24, size)
        
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            
        
            if frame is not None:
                frame_ = self.rescale_frame(frame, percent=75)
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
            height, width, d = image.shape
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                
                # Get coordinates
                hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankle = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                #print("flag is {}".format(flag))
               
                # Calculate anglej
                angle = self.calculate_angle(shoulder, elbow, wrist)
                
                angle_knee = self.calculate_angle(hip, knee, ankle) #Knee joint angle
                angle_knee = round(angle_knee,2)
                
                angle_hip = self.calculate_angle(shoulder, hip, knee)
                angle_hip = round(angle_hip,2)
                
                hip_angle = 180-angle_hip       
                knee_angle = 180-angle_knee    
                
                
                angle_min.append(angle_knee)
                angle_min_hip.append(angle_hip)
                
                
                
                
                # Rep counter logic
                if int(hip[1]*height)>self.y_knee_ref:
                    stage = "up" 
                    #print("-----stage is up------"*200)
                if hip[1]*height<=self.y_hip_ref and stage == "up": 
                    stage = "down"   
                    counter+=1 
                    print("1 more rep completed!!!")
            except:
                print("Error occured!!!!!!")
                pass
    
                    
            # Render detections
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                    self.mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2), 
                                    self.mp_drawing.DrawingSpec(color=(203,17,17), thickness=2, circle_radius=2) 
                                    )               
            
            #width, height, d = image.shape
            #out.write(image)
        

            image = cv2.line(image, (0, int(hip[1]*height)), (width, int(hip[1]*height)), (0, 0, 255))

            image = cv2.line(image, (0, int(self.y_hip_ref)), (width, int(self.y_hip_ref)), (0, 255, 0))
            #print(int(hip[1]*height), width)
            image = cv2.line(image, (0, int(self.y_knee_ref)), (width, int(self.y_knee_ref)), (0, 255, 0))
            image = cv2.line(image, (0, int((knee[1])*height)), (width, int(knee[1]*height)), (0, 0, 255))
            
            return image, counter, stage
        








