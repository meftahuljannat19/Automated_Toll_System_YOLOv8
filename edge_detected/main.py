import cv2
import numpy as np
import imutils
import easyocr
import pandas as pd
from cvzone.SerialModule import SerialObject
from time import sleep
img = cv2.imread('Cars111.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow("CarGray",cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
#cv2.waitKey(1)
bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(bfilter, 30, 200)
#cv2.imshow("CarEdge",cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
#cv2.waitKey(1)
keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0,255,-1)
new_image = cv2.bitwise_and(img, img, mask=mask)
#cv2.imshow("NumberPlate",cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
#cv2.waitKey(1)
(x,y) = np.where(mask==255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1:x2+1, y1:y2+1]
#cv2.imshow("NumberPlateCropped",cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
#cv2.waitKey(1)
reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_image, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ')
print(result)
text = result[0][1]
font = cv2.FONT_HERSHEY_SIMPLEX
res = cv2.putText(img, text=text, org=(approx[0][0][1], approx[1][0][0]), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
cv2.imshow("Image",res)
cv2.waitKey(1)
data = pd.read_csv('Balance_Sheet.csv')
license = data.iloc[:,1:-1]
balance = data.iloc[:,-1]
print(license)
is_correct = text in data['License_Plate'].values
arduino = SerialObject("COM4")
if is_correct:
    print(f"The value '{text}' is correct.")
    data.loc[data['License_Plate'] == text, 'Balance'] -= 100
    data.to_csv('Balance_Sheet.csv',index=False)
    while True:
        arduino.sendData([1])
        sleep(0.01)
