import math
import os
import sys
import face_recognition
import cv2
import numpy as np


def face_confidence(face_distance, face_match_threshold=0.6):
    face_range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (face_range * 2)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encoding = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()
        # encode faces

    def encode_faces(self):
        for image in os.listdir('../Faces'):
            face_image = face_recognition.load_image_file(f'../Faces/{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encoding.append(face_encoding)
            self.known_face_names.append(image)

        print(self.known_face_names)

    def run_image_recognition(self, face):
        resized_face = cv2.resize(face, (0, 0), fx=0.25, fy=0.25)
        rgb_face = resized_face[:, :, ::-1]

        self.face_locations = face_recognition.face_locations(rgb_face)
        self.face_encodings = face_recognition.face_encodings(resized_face, self.face_locations)

        self.face_names = []
        for face_encoding in self.face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encoding, face_encoding)
            name = 'Unknown'
            confidence = 'Unknown'

            face_distances = face_recognition.face_distance(self.known_face_encoding, face_encoding)
            best_math_index = np.argmin(face_distances)

            if matches[best_math_index]:
                name = self.known_face_names[best_math_index]
                confidence = face_confidence(face_distances[best_math_index])

            self.face_names.append(f'{name} ({confidence})')

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found')

        while True:
            ret, frame = video_capture.read()

            if self.process_current_frame:
                self.run_image_recognition(frame)

            self.process_current_frame = not self.process_current_frame

            # Display annotations
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                left *= 4
                bottom *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)

            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        video_capture.release()
        cv2.destroyWindow()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
