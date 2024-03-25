import face_recognition
import os, sys
import cv2
import numpy as np
import math
from datetime import datetime

class FaceRecognition:
    known_face_encodings = []
    known_face_names = []

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image_file in os.listdir('./client/src/foto'):
            image_path = os.path.join('./client/src/foto', image_file)
            face_image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(face_image)
            
            if len(face_encodings) > 0:
                face_encoding = face_encodings[0]  # Assuming only one face per image
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(image_file)
            else:
                print(f"No face detected in {image_file}. Skipping...")
        
        print(self.known_face_names)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)
    
        if not video_capture.isOpened():
            sys.exit('Video source not found...')
        
        while True:
            ret, frame = video_capture.read()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                confidence = '???'

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    face_distance = face_distances[best_match_index]
                    if face_distance < 0.9:
                        confidence = self.face_confidence(face_distance)
                        if confidence > 95:
                            name = self.known_face_names[best_match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, f'{name} ({confidence})', (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    @staticmethod
    def face_confidence(face_distance, face_match_threshold=0.8):
        range_val = (1.2 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range_val * 2.0)

        if face_distance > face_match_threshold:
            return round(linear_val * 100, 2)
        else:
            value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
            return round(value, 2)

if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
