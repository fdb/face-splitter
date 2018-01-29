import os
import numpy as np
import cv2 as cv

def angle(x0, y0, x1, y1):
    from math import degrees, atan2
    a = degrees( atan2(y1-y0, x1-x0) )
    return a

def coordinates(x0, y0, distance, angle):
    from math import radians, sin, cos
    x1 = x0 + cos(radians(angle)) * distance
    y1 = y0 + sin(radians(angle)) * distance
    return x1, y1

face_cascade = cv.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
# eye_cascade = cv.CascadeClassifier('classifiers/haarcascade_eye.xml')


def split_face(filename, index):

    img = cv.imread(filename)
    #img = cv.resize(img,None,fx=0.2, fy=0.2, interpolation = cv.INTER_CUBIC)
    (img_w, img_h, _) = img.shape

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) != 1:
        print('File %s: %d faces detected. Skipping...' % (filename, len(faces)))
        return False
    x,y,w,h = faces[0]

    # Enlarge the face (OpenCV just looks at the face not the hair)
    dy = int(h * 0.2)
    y -= dy
    h += dy
    #cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    #cv.rectangle(img,(x,y), (x+w,int(y+h/2)), (255, 0, 0), 2)

    # Divide into thirds
    third_h = h / 3
    top_third_y = int(y + h / 3)
    bot_third_y = int(y + third_h * 2)

    #cv.line(img,(x, top_third_y), (x + w, top_third_y), (255, 0, 0), 1)
    #cv.line(img,(x, bot_third_y), (x + w, bot_third_y), (255, 0, 0), 1)

    top_third = img[y:top_third_y, x:x+w]
    mid_third = img[top_third_y:bot_third_y, x:x+w]
    bot_third = img[bot_third_y:y+h, x:x+w]

    fname = os.path.basename(filename)
    print(fname)
    fname, ext = os.path.splitext(fname)
    cv.imwrite("%s/face_%d_t%s" % (OUTPUT_DIR, index, ext), top_third)
    cv.imwrite("%s/face_%d_m%s" % (OUTPUT_DIR, index, ext), mid_third)
    cv.imwrite("%s/face_%d_b%s" % (OUTPUT_DIR, index, ext), bot_third)

    # roi_gray = gray[y:y+h, x:x+w]
    # roi_color = img[y:y+h, x:x+w]
    # eyes = eye_cascade.detectMultiScale(roi_gray)
    # assert len(eyes) >= 2, "detected %s eyes" % eyes
    # ex1,ey1,ew1,eh1 = eyes[0]
    # ex2,ey2,ew2,eh2 = eyes[1]
    # ex1 += x
    # ey1 += y
    # ex2 += x
    # ey2 += y
    # ecx1, ecy1 = (int(ex1 + ew1 / 2), int(ey1 + eh1 / 2))
    # ecx2, ecy2 = (int(ex2 + ew2 / 2), int(ey2 + eh2 / 2))
    # cv.line(img, (ecx1, ecy1), (ecx2, ecy2), (0, 255, 0), 2)
    # cv.rectangle(roi_color,(ecx-2, ecy-2),(ecx+2, ecy+2),(0,255,0),2)

    # fcx = int((ecx1 + ecx2) / 2)
    # fcy = int((ecy1 + ecy2) / 2)
    # eye_angle = angle(ecx1, ecy1, ecx2, ecy2)
    # print("Eye Angle:", eye_angle)
    # print("Detected center vs real center:", int(y + h / 2), fcy)

    # dy = int(y + h / 2) - fcy
    # face_height = h +  dy
    # Calculate bottom center of face
    #face_height = int(h + ((y + h/2) - fcy))
    # fbx, fby = [int(c) for c in coordinates(fcx, fcy, face_height / 2, eye_angle - 90)]
    # cv.line(img, (fcx, fcy), (fbx, fby), (0, 255, 0), 2)

    # # Calculate top center of face
    # ftx, fty = [int(c) for c in coordinates(fcx, fcy, face_height / 2, eye_angle + 90)]
    # cv.line(img, (fcx, fcy), (ftx, fty), (0, 255, 0), 2)



    #cv.imshow('img',img)
    #cv.waitKey(0)
    #cv.destroyAllWindows()
    return True

#split_face('faces/9240516728_9975536b25_o.jpg')

def usage():
    print("python3 split_faces.py INPUT_DIR OUTPUT_DIR [index]")

import sys
if len(sys.argv) < 3:
    usage()
    sys.exit(-1)

INPUT_DIR = sys.argv[1]
OUTPUT_DIR = sys.argv[2]
if len(sys.argv) == 4:
    try:
        index = int(sys.argv[3])
    except ValueError:
        print("Given index '%s' is not a number." % sys.argv[3])
        sys.exit(-1)
else:
    index = 1

try:
    os.makedirs(OUTPUT_DIR)
except FileExistsError:
    pass

with os.scandir(INPUT_DIR) as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_file():
            print(entry.name)
            ok = split_face(os.path.join(INPUT_DIR, entry.name), index)
            if ok:
                index += 1
