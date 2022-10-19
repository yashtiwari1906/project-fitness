
import cv2
from cv2 import destroyAllWindows
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle


def rescale_frame(frame, percent=50):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    try:
        return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)
    except:
        print("frame was empty!!!") 
        return frame

# Youtube video

def pose_detection_mediapipe(frame, flag, y_hip_ref, y_knee_ref, counter, stage):
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
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        
    
        #if frame is not None:
            #frame_ = rescale_frame(frame, percent=75)
        
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
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            
            # Get coordinates
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            #print("flag is {}".format(flag))
            if flag:
                y_hip_ref = hip[1]*height + hip[1]*(8/100)*height
                y_knee_ref = knee[1]*height - knee[1]*(8/100)*height   
                flag = False                                           
            
            # Calculate anglej
            angle = calculate_angle(shoulder, elbow, wrist)
            
            angle_knee = calculate_angle(hip, knee, ankle) #Knee joint angle
            angle_knee = round(angle_knee,2)
            
            angle_hip = calculate_angle(shoulder, hip, knee)
            angle_hip = round(angle_hip,2)
            
            hip_angle = 180-angle_hip       
            knee_angle = 180-angle_knee    
            
            
            angle_min.append(angle_knee)
            angle_min_hip.append(angle_hip)
            
            #print(angle_knee)
            # Visualize angle
            """cv2.putText(image, str(angle), 
                        tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )"""
                    
                
            cv2.putText(image, str(angle_knee), 
                        tuple(np.multiply(knee, [1500, 800]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                                )
            
            cv2.putText(image, str(angle_hip), 
                        tuple(np.multiply(hip, [1500, 800]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            
            
            # Curl counter logic

            if int(hip[1]*height)>y_knee_ref:
                stage = "up" 
                #print("-----stage is up------"*200)
            if hip[1]*height<=y_hip_ref and stage == "up": 
                stage = "down"   
                counter+=1 
                print("1 more rep completed!!!")




            """
            if angle_knee > 169:
                stage = "up"
            if angle_knee <= 90 and stage =='up':
                stage="down"
                counter +=1
                print(counter)
                min_ang  =min(angle_min)
                max_ang = max(angle_min)
                
                min_ang_hip  =min(angle_min_hip)
                max_ang_hip = max(angle_min_hip)
                
                print(min(angle_min), " _ ", max(angle_min))
                print(min(angle_min_hip), " _ ", max(angle_min_hip))
                angle_min = []
                angle_min_hip = []
            """
        except:
            print("Error occured!!!!!!")
            pass
        
        # Render squat counter
        # Setup status box
        cv2.rectangle(image, (20,20), (435,160), (0,0,0), -1)
        
        # Rep data
        """cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)"""
        cv2.putText(image, "Repetition : " + str(counter), 
                    (30,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        """cv2.putText(image, 'STAGE', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)"""
        """cv2.putText(image, stage, 
                    (10,120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)"""
        
        #Knee angle:
        """cv2.putText(image, 'Angle', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)"""
        cv2.putText(image, "Knee-joint angle : " + str(min_ang), 
                    (30,100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        #Hip angle:
        cv2.putText(image, "Hip-joint angle : " + str(min_ang_hip), 
                    (30,140), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        

        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(203,17,17), thickness=2, circle_radius=2) 
                                )               
        
        #width, height, d = image.shape
        #out.write(image)
    

        image = cv2.line(image, (0, int(hip[1]*height)), (width, int(hip[1]*height)), (0, 0, 255))

        image = cv2.line(image, (0, int(y_hip_ref)), (width, int(y_hip_ref)), (0, 255, 0))
        #print(int(hip[1]*height), width)
        image = cv2.line(image, (0, int(y_knee_ref)), (width, int(y_knee_ref)), (0, 255, 0))
        image = cv2.line(image, (0, int((knee[1])*height)), (width, int(knee[1]*height)), (0, 0, 255))
        
        return image, y_hip_ref, y_knee_ref, counter, stage
        







if __name__ == "__main__":
    cap = cv2.VideoCapture("youTube_video.mp4")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (640, 480)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output_video_.avi', fourcc, 24, size)
    flag = True

    

    flag = True 
    counter = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if flag:
            im, y_hip_ref, y_knee_ref, counter, stage = pose_detection_mediapipe(frame, flag, 0, 0, counter, None) 
            flag = False
        else: 
            im, y_hip_ref, y_knee_ref, counter, stage = pose_detection_mediapipe(frame, flag, y_hip_ref, y_knee_ref, counter, stage) 
            print(counter)
        cv2.imshow("image", im)


        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            #break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    