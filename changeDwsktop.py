import cv2
import mediapipe as mp
import pyautogui

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize MediaPipe hands solution
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Variables to store previous wrist position
prev_x = 0
prev_y = 0
initial_frame = True

# Function to switch desktop
def switch_desktop(direction):
    if direction == 'left':
        pyautogui.hotkey('ctrl', 'win', 'left')
    elif direction == 'right':
        pyautogui.hotkey('ctrl', 'win', 'right')

while True:
    success, img = cap.read()  # Capture an image from the camera
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert the image to RGB
    
    # Process the image and get hand landmark results
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:  # If hand landmarks are detected
        for handlandmark in results.multi_hand_landmarks:
            for id, lm in enumerate(handlandmark.landmark):
                # Get the wrist joint point
                if id == 0:
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if initial_frame:
                        prev_x, prev_y = cx, cy
                        initial_frame = False
                    else:
                        # Detect swipe motion
                        if cx - prev_x > 50:  # Swipe right
                            switch_desktop('right')
                            prev_x, prev_y = cx, cy
                        elif prev_x - cx > 50:  # Swipe left
                            switch_desktop('left')
                            prev_x, prev_y = cx, cy

            mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

    cv2.imshow('Image', img)  # Display the image

    if cv2.waitKey(1) & 0xFF == ord(' '):  # Exit the loop when spacebar is pressed
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close all OpenCV windows
