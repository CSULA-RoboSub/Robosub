import cv2
import utils

frame =  cv2.imread('dice_test_data/dice1521499707100.jpg')

lab =  cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)

l,a,b = cv2.split(lab)

while True:

    clahe = cv2.createCLAHE(3.0, (8,8))
    cl =  clahe.apply(l)

    limg = cv2.merge((cl,a,b))

    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,100,200)

    im, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boxes = [cv2.boundingRect(c) for c in contours ]

    rois = [b for b in boxes if b[2] * b[3] > 200]

    for x, y, w, h in rois:
        cv2.rectangle(final, (x, y), (x+w, y+h), utils.colors["blue"], 3)

    cv2.imshow('basic_edges',cv2.Canny(frame,100,200))
    cv2.imshow('edges',edges)
    cv2.imshow('gray',gray)
    cv2.imshow('final',final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
