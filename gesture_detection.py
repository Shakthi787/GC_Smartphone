# === gesture_detection.py ===
import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
last_processed = 0

def detect_hand_sign(image):
    global last_processed
    image = cv2.flip(image, 1)
    current_time = time.time()
    if current_time - last_processed < 0.3:
        return None, image
    last_processed = current_time

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)
    gesture = None
    annotated_image = image.copy()

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            gesture = detect_gesture(landmarks)
            mp.solutions.drawing_utils.draw_landmarks(
                annotated_image, landmarks, mp_hands.HAND_CONNECTIONS)

    return gesture, annotated_image


def detect_gesture(landmarks):
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    if thumb_tip.y < index_tip.y:
        return "THUMBS_UP"
    elif all(tip.y > index_tip.y for tip in [thumb_tip, middle_tip, ring_tip, pinky_tip]):
        return "FIST"
    elif all(tip.y < index_tip.y for tip in [thumb_tip, index_tip, middle_tip]):
        return "THREE_FINGERS"
    elif all(tip.y < index_tip.y for tip in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]):
        return "PALM"
    elif thumb_tip.x < index_tip.x:
        return "SWIPE_LEFT"
    elif thumb_tip.x > index_tip.x:
        return "SWIPE_RIGHT"
    elif abs(thumb_tip.x - index_tip.x) < 0.02 and abs(thumb_tip.y - index_tip.y) < 0.02:
        return "OK_SIGN"
    elif index_tip.y < middle_tip.y and ring_tip.y > pinky_tip.y:
        return "VICTORY"

    return None