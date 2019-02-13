import cv2
from preference import *
aruco = cv2.aruco

pixel_per_onebox = 256

boardImage=0
boardImage = board.draw((pixel_per_onebox*5,pixel_per_onebox*8), boardImage, 0, 1)
cv2.imwrite("charuco2.bmp", boardImage)
cv2.imshow("charuco", boardImage)
cv2.waitKey(0)
cv2.destroyAllWindows()