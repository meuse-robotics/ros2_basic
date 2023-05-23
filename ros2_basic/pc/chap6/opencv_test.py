import cv2

cap = cv2.VideoCapture(2)

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('cam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()