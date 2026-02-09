import cv2

face_cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detect_face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

    for (x, y, w, h) in detect_face:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 125, 100), 3)

    cv2.imshow("Detected", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
