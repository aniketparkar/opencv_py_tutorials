import cv2
import numpy as np

lower_hue = 0
upper_hue = 179

lower_sat = 0
upper_sat = 255

lower_val = 0
upper_val = 255


def a_lower_hue(x):
    global lower_hue
    lower_hue = x

def a_upper_hue(x):
    global upper_hue
    upper_hue = x

def a_lower_sat(x):
    global lower_sat
    lower_sat = x

def a_upper_sat(x):
    global upper_sat
    upper_sat = x

def a_lower_val(x):
    global lower_val
    lower_val = x

def a_upper_val(x):
    global upper_val
    upper_val = x

def main():
    cap = cv2.VideoCapture(0)

    _, frame = cap.read()
    cv2.imshow('res', frame)

    cv2.createTrackbar('lower hue', 'res', 0, 179, a_lower_hue)
    cv2.createTrackbar('upper hue', 'res', upper_hue, 179, a_upper_hue)
    cv2.createTrackbar('lower sat', 'res', 0, 255, a_lower_sat)
    cv2.createTrackbar('upper sat', 'res', upper_sat, 255, a_upper_sat)
    cv2.createTrackbar('lower val', 'res', 0, 255, a_lower_val)
    cv2.createTrackbar('upper val', 'res', upper_val, 255, a_upper_val)



    while(1):

        # Take each frame

        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # define range of blue color in HSV
        lower_blue = np.array([lower_hue, lower_sat, lower_val])
        upper_blue = np.array([upper_hue, upper_sat, upper_val])
        
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

main()

if __name__ == '__main__':
    main()
