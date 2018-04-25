import cv2
import numpy
import matplotlib.pyplot as plt

frame = cv2.imread('dice_test_data/dice1521499317210.jpg')

lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)

l,a,b = cv2.split(lab)
clahe = cv2.createCLAHE(3.0, (8,8))
cl = clahe.apply(l)
limg = cv2.merge((cl,a,b))

final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,100,200)

plt.imshow(final)
plt.show()

im, contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

plt.imshow(edges)
plt.show()

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
        cv2.drawContours(frame, [cnt], 0, (0, 0, 255), -1)

plt.imshow(frame)
plt.show()