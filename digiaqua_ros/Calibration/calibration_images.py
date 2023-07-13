#!/usr/bin/python3

import cv2
def main():

    cap = cv2.VideoCapture(4)
    cap2 = cv2.VideoCapture(2)

    num = 0

    while cap.isOpened():

        succes1, img = cap.read()
        succes2, img2 = cap2.read()

        k = cv2.waitKey(5)

        if k == 27:
            break
        elif k == ord('s'):  # wait for 's' key to save and exit
            cv2.imwrite('/home/vinicius/catkin_ws/src/DigiAqua/digiaqua_ros/Calibration/Calibration_Images/stereoLeft/imageL' + str(num) + '.png', img)
            cv2.imwrite('/home/vinicius/catkin_ws/src/DigiAqua/digiaqua_ros/Calibration/Calibration_Images/stereoRight/imageR' + str(num) + '.png', img2)
            print("images saved!")
            num += 1

        cv2.imshow('Img 1', img)
        cv2.imshow('Img 2', img2)

if __name__ == '__main__':
    main()