#!/usr/bin/python3
import cv2
import numpy as np

def create_mask(image_path, target_color):
    # Read the image
    original_image = cv2.imread(image_path)

    # Color channels extraction (BGR)
    blue_channel, green_channel, red_channel = cv2.split(original_image)

    # Define the lower and upper limit for the target color
    lower_bound = np.array(target_color[:3] - [30, 20, 20], dtype=np.uint8)
    upper_bound = np.array(target_color[:3] + [30, 20, 55], dtype=np.uint8)

    # Create a mask for the target color
    color_mask = cv2.inRange(original_image, lower_bound, upper_bound)

    # Image binarization
    binary_image = np.zeros_like(color_mask)
    binary_image[color_mask > 0] = 255

    # Find the contours
    contornos, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contorno in contornos:
        # Fit an ellipse in the contour
        elipse = cv2.fitEllipse(contorno)

        # Get the Ellipse Orientation
        orientacao = elipse[2]

        print(f'Orientação: {orientacao} graus')

        # Define the rotation angle necessary to fix the orientation
        angulo_correcao = orientacao

        # Get the bounding box for the object
        caixa_delimitadora = cv2.boundingRect(contorno)
        x, y, w, h = caixa_delimitadora

        # Get the bounding box center
        centro_caixa = (x + w // 2, y + h // 2)

        # Create the transforming matrix of rotation
        matriz_rotacao = cv2.getRotationMatrix2D(centro_caixa, angulo_correcao, 1.0)

        # Apply the transformation only in detected object
        objeto_rotacionado = cv2.warpAffine(binary_image, matriz_rotacao, (binary_image.shape[1], binary_image.shape[0]))

        # Find contours in rotationed image
        contornos2, _ = cv2.findContours(objeto_rotacionado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw a bounding box in each founded object
        for contorno2 in contornos2:
            x2, y2, w2, h2 = cv2.boundingRect(contorno2)
            cv2.rectangle(objeto_rotacionado, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 255), 2)

    # Oyster size
    print(f'Largura: {w} mm, Altura: {h} mm')

    # Show the images
    cv2.imshow('Original', original_image)
    cv2.imshow('Binary', binary_image)
    cv2.imshow('Obj Rotacionado', objeto_rotacionado)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
        # Image path
        image_path = '/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/output/oyster4.jpg'

        # Target collor (pure blue with 80% transparency)
        target_color = np.array([30, 20, 200], dtype=np.uint8)

        # Create the mask and show the image with the bounding box
        create_mask(image_path, target_color)

if __name__ == "__main__":
        main()

# Resultados:
#
# Oyster 1: Largura: 46 mm, Altura: 101 mm
# Oyster 2: Largura: 70 mm, Altura: 38 mm
# Oyster 3: Largura: 54 mm, Altura: 68 mm
# Oyster 4: Largura: 62 mm, Altura: 78 mm
# Oyster 5: Largura: 46 mm, Altura: 80 mm

# Fator de conversao Pixel/mm
# Objeto padrao 1: 41x41 pixeis / Tamanho real: 40x40 mm
# Objeto padrao 2: 47x17 / Tamanho real: 47x16
# Logo, pra 72cm de altura da camera, 1mm ~ 1 pixel