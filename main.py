import cv2
import mediapipe as mp
import pygame

mpManos = mp.solutions.hands
mpTrazoMano = mp.solutions.drawing_utils

pygame.mixer.init()
"""sounds = [
    pygame.mixer.Sound("#fa.wav"), #INDICE IZQUIERDO
    pygame.mixer.Sound("la.wav"), #Medio izquierdo
    pygame.mixer.Sound("re.wav"), #Anular IZQUIERDO
    pygame.mixer.Sound("#do.wav"), #INDICE Derecho
    pygame.mixer.Sound("#sol.wav"), #MEDIO Derecho
    pygame.mixer.Sound("si.wav"), #Anular Derecho
    
    
]""" #Se penso agregar sonidos al bajar dedo. Idea descartada.

def is_finger_down(landmarks, finger_tip, finger_mcp):
    return landmarks[finger_tip].y > landmarks[finger_mcp].y

cap = cv2.VideoCapture(0) #Indice 0, del video es 1. se debe a que el tiene 2 camaras, yo una. Probablemente es el 0, sino cambiar

with mpManos.Hands(min_detection_confidence = 0.5, min_tracking_confidence = 0.5, 
                   max_num_hands = 6) as hands: 
    finger_state = [False]*6
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame - cv2.flip(frame,1)
        rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #Invertimos la escala de color para evitar resultados inesperados. MP trabaja RGB, cv2 con BGR.
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mpTrazoMano.draw_landmarks(frame, hand_landmarks, mpManos.HAND_CONNECTIONS)

        cv2.imshow('Hand detection', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
                