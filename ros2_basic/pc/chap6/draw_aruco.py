import cv2
from cv2 import aruco

dictionary = aruco.Dictionary_get(aruco.DICT_4X4_50)
size = 100

for id in range(5):
    mark = aruco.drawMarker(dictionary, id, size)
    label = f"id_{id:02}"
    #cv2.imshow(label, mark)
    cv2.imwrite(label + ".png", mark)
    cv2.waitKey(0)

cv2.destroyAllWindows()
