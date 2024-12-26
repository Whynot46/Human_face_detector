import cv2
import numpy as np
from ultralytics import YOLO


model = YOLO("./yolo_models/yolov10s.pt")
capture = cv2.VideoCapture(0)

 
def find_peoples(frame):
    results = model(frame)
    gray_frame = gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for result in results:
        boxes = result.boxes  
        for box in boxes:
            cls = int(box.cls[0])
            if model.names[cls] == 'person':
                x_1, y_1, x_2, y_2 = map(int, box.xyxy[0])
                probability = float(box.conf[0])
                if probability > 0.5:
                    cv2.rectangle(frame, (x_1, y_1), (x_2, y_2), (255, 0, 0), 2)
                    cv2.putText(frame, f'person {probability:.2f}', (x_1, y_1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)            
    return frame


def main_loop():
    while True:
        ret, frame = capture.read()
        if not ret:
            break  

        peoples_frame = find_peoples(frame)
        
        cv2.imshow('YOLOv10', peoples_frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        
    capture.release()
    cv2.destroyAllWindows()
    

if __name__=="__main__":
    main_loop()