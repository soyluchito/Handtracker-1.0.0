import cv2
import mediapipe as mp
import pygame

mpManos = mp.solutions.hands
mpTrazoMano = mp.solutions.drawing_utils

pygame.mixer.init()

def is_finger_down(landmarks, finger_tip, finger_mcp):
    return landmarks[finger_tip].y > landmarks[finger_mcp].y

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow("HandTracker 1.0.0", cv2.WINDOW_NORMAL)
cv2.resizeWindow("HandTracker 1.0.0", 1280, 720)

with mpManos.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=6
) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mpTrazoMano.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mpManos.HAND_CONNECTIONS
                )

        cv2.imshow("HandTracker 1.0.0", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()