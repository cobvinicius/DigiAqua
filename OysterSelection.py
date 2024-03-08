#!/usr/bin/python3

from fastsam import FastSAM, FastSAMPrompt
import torch
import cv2
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def click_event(event, a, b, flags, params):
    global x, y
    if event == cv2.EVENT_LBUTTONDOWN:
        x, y = a, b
        print(a, ' ', b)


def get_bbox_from_mask(mask):
    mask = mask.astype(np.uint8)
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    x1, y1, w, h = cv2.boundingRect(contours[0])
    x2, y2 = x1 + w, y1 + h
    if len(contours) > 1:
        for b in contours:
            x_t, y_t, w_t, h_t = cv2.boundingRect(b)
            # 将多个bbox合并成一个
            x1 = min(x1, x_t)
            y1 = min(y1, y_t)
            x2 = max(x2, x_t + w_t)
            y2 = max(y2, y_t + h_t)
        h = y2 - y1
        w = x2 - x1
    return [x1, y1, x2, y2]

# def segment_image(image, bbox):
#     image_array = np.array(image)
#     segmented_image_array = np.zeros_like(image_array)
#     x1, y1, x2, y2 = bbox
#     segmented_image_array[y1:y2, x1:x2] = image_array[y1:y2, x1:x2]
#     segmented_image = Image.fromarray(segmented_image_array)
#     black_image = Image.new("RGB", image.size, (255, 255, 255))
#     # transparency_mask = np.zeros_like((), dtype=np.uint8)
#     transparency_mask = np.zeros(
#         (image_array.shape[0], image_array.shape[1]), dtype=np.uint8
#     )
#     transparency_mask[y1:y2, x1:x2] = 255
#     transparency_mask_image = Image.fromarray(transparency_mask, mode="L")
#     black_image.paste(segmented_image, mask=transparency_mask_image)
#     return black_image

def main():

    IMAGE_PATH = '/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/Capture/frame_2.png'
    # IMAGE_PATH = '/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/Capture/frame_3.png'
    # IMAGE_PATH = '/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/Capture/frame_4.png'

    img = cv2.imread(IMAGE_PATH, 1)

    cv2.imshow('image', img)

    cv2.setMouseCallback('image', click_event)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

    ################################

    model = FastSAM('FastSAM-x.pt')
    DEVICE = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )

    everything_results = model(
        IMAGE_PATH,
        device=DEVICE,
        retina_masks=True,
        imgsz=1024,
        conf=0.4,
        iou=0.9,
    )

    prompt_process = FastSAMPrompt(IMAGE_PATH, everything_results, device=DEVICE)
    ann = prompt_process.everything_prompt()
    # ann = prompt_process.point_prompt(points=[[x, y]], pointlabel=[1])

    prompt_process.plot(
        annotations=ann,
        output_path='/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/output/oyster_all.jpg',
        # output_path='/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/output/frame_1.png',
        mask_random_color=True,
        better_quality=True,
        retina=False,
        withContours=True,
    )

    # bbox = get_bbox_from_mask(ann[0])

    # print(DEVICE)
    # print(bbox)

    im = Image.open('/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/output/oyster_all.jpg')

    # Converta a imagem para NumPy array
    # im = np.array(img)

    # Create figure and axes
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(im)

    # # Create a Rectangle patch
    # rect = patches.Rectangle((bbox[0],bbox[1]), (bbox[2] - bbox[0]), (bbox [3] - bbox[1]), linewidth=1, edgecolor='b', facecolor='none')
    #
    # # Add the patch to the Axes
    # ax.add_patch(rect)

    plt.show()

if __name__ == '__main__':
    main()
