

#########################################################
#  ARQUIVO COM O CODIGO DE PRE PROCESSAMENTO DA IMAGEM  #
#########################################################

import cv2
import numpy as np


def PreProcessamento(imagem):

    # tranforma a imagem em escala de cinza
    img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # aplica gaussian blur
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)

    # detecao de contorno com algoritmo de Canny
    img_canny = cv2.Canny(img_blur, 10, 50)

    return img_canny
