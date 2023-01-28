import cv2
import imutils

def npary(flipped=True):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if flipped:
        return imutils.resize(cv2.rotate(frame, cv2.ROTATE_180))
    return frame

def toGreyScale(frame):
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(grey, (21, 21), 0)

def isOccupied(firstFrame, frame):
    grey0 = toGreyScale(firstFrame)
    grey1 = toGreyScale(frame)

    frameDelta = cv2.absdiff(grey0, grey1)
    thresh = cv2.threshold(frameDelta, thresh=30, maxval=255, type=cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=1)
    cnts = cv2.findContours(thresh.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c) > 2000:
            return True

    return False
