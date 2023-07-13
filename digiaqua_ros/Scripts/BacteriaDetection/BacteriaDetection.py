#!/usr/bin/python3

import cv2
import numpy as np

def main():

    # Carregar Imagem
    rgbImage = cv2.imread('/7-1.tif')

    # Converte a imagem para escala de cinza
    grayImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)

    # define o valor do threshold
    threshold_value = 89

    # binariza a imagem usando o valor do threshold
    _, binaryImage = cv2.threshold(grayImage, threshold_value, 255, cv2.THRESH_BINARY)

    # Calcula o número de pixels pretos na imagem binária
    numPixelsPretos = np.sum(binaryImage == 0)

    # Obtém o número de linhas e colunas da imagem binária
    numLinhas, numColunas = binaryImage.shape

    # Calcula o número total de pixels na imagem binária
    numPixelsTotal = numLinhas * numColunas

    # Calcula a porcentagem de pixels pretos na imagem binária
    percentPixelsPretos = (numPixelsPretos / numPixelsTotal) * 100

    # Exibe a porcentagem de pixels pretos
    print('Porcentagem de pixels pretos: {:.2f}%'.format(percentPixelsPretos))

    # Exibe as imagens

    cv2.namedWindow('RGB Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('RGB Image', 800, 600)

    cv2.namedWindow('Binary Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Binary Image', 800, 600)

    cv2.imshow('RGB Image', rgbImage)
    cv2.imshow('Binary Image', binaryImage)

    # Aguarda uma tecla ser pressionada para fechar as janelas
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()