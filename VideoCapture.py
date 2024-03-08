#!/usr/bin/python3


# import the opencv library
import cv2

def main():

    # define a video capture object
    import cv2

    # Capture video from webcam
    vid_capture = cv2.VideoCapture(2)
    vid_capture2= cv2.VideoCapture(4)
    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter("/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/Capture/Videos/Vitorino/video_vitorino_turbidez3.avi", vid_cod, 20.0, (640, 480))
    output2 = cv2.VideoWriter("/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/Capture/Videos/Vitorino/video_vitorino_turbidez4.avi", vid_cod, 20.0,
                              (640, 480))

    while (True):
        # Capture each frame of webcam video
        ret, frame = vid_capture.read()
        ret2, frame2 = vid_capture2.read()
        cv2.imshow("My cam video", frame)
        cv2.imshow("My cam video", frame2)
        output.write(frame)
        output2.write(frame2)
        # Close and break the loop after pressing "x" key
        if cv2.waitKey(1) & 0XFF == ord('x'):
            break

    # close the already opened camera
    vid_capture.release()
    vid_capture2.release()
    # close the already opened file
    output.release()
    output2.release()
    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

# Obs - Video 2 em diante: stereo vision

if __name__ == '__main__':
    main()
