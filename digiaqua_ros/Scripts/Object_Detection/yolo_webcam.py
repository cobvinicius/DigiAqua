#!/usr/bin/python3

from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2

def main():

    # Load a model
    # model = YOLO("yolov8n.yaml")  # build a new model from scratch
    # model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

    model = YOLO("best.pt")  # load a pretrained model (recommended for training)

    # # Use the model
    # model.train(data="coco128.yaml", epochs=3)  # train the model
    # metrics = model.val()  # evaluate model performance on the validation set
    # results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
    # path = model.export(format="onnx")  # export the model to ONNX format

    results = model.predict(source="0", show=True)

    print(results)

if __name__ == '__main__':
    main()