import cv2
from ultralytics import YOLO


class Capture(object):
    width = 1280
    height = 720
    model = YOLO("./yolo_models/yolov10s.pt")
    capture_stream = 0  # 0 - вебкамера
    last_frame = None

    def __init__(self):
        self.video = cv2.VideoCapture(self.capture_stream)

    def __del__(self):
        self.video.release()

    def find_peoples(self, frame):
        results = self.model(frame)
        for result in results:
            boxes = result.boxes  
            for box in boxes:
                cls = int(box.cls[0])
                if self.model.names[cls] == 'person':
                    x_1, y_1, x_2, y_2 = map(int, box.xyxy[0])
                    probability = float(box.conf[0])
                    if probability > 0.5:
                        cv2.rectangle(frame, (x_1, y_1), (x_2, y_2), (255, 0, 0), 2)
                        cv2.putText(frame, f'person {probability:.2f}', (x_1, y_1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)            
        return frame

    async def get_frame(self):
        ret, frame = self.video.read()
        if not ret:
            return None
        processed_frame = self.find_peoples(frame)
        self.last_frame = processed_frame  # Сохраняем последний кадр
        cut_frame = cv2.resize(processed_frame, (self.width, self.height))
        ret, jpeg = cv2.imencode('.jpg', cut_frame)
        return jpeg.tobytes()
    
    
    async def get_last_frame(self):
        ret, jpeg = cv2.imencode('.jpg', self.last_frame)
        return jpeg