import cv2 

face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('models/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('models/haarcascade_smile.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_detect = face_cascade.detectMultiScale(gray, scaleFactor=2.0, minNeighbors=5)
    
    for (x, y, w, h) in face_detect:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3) 
        cv2.putText(frame, "Face", (x+50, y-30), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0, 100, 0), 4)   
        Region_of_Interest_gray = gray[y:y+h, x:x+w]
        Region_of_Interest_color = frame[y:y+h, x:x+w]

        eye_detect = eye_cascade.detectMultiScale(Region_of_Interest_gray, scaleFactor=1.1, minNeighbors=25)
        for (x, y, w, h) in eye_detect:
            cv2.rectangle(Region_of_Interest_color, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.putText(frame, "eye", (x-100, y+100), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (100, 0, 0), 3)

        smile_detect = smile_cascade.detectMultiScale(Region_of_Interest_color, scaleFactor=1.1, minNeighbors=25)
        for (x, y, w, h) in smile_detect:
             cv2.rectangle(Region_of_Interest_color, (x, y), (x+w, y+h), (0, 0, 255), 3)
             cv2.putText(frame, "smile", (x+30, y-30), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 100), 3)

    cv2.imshow("Detected", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()