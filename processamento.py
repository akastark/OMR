import cv2
import numpy as np


def reordena(pontos):

    pontos = pontos.reshape((4, 2))

    # matriz com pontos reordenados
    pontos_aux = np.zeros((4, 1, 2), np.int32)
    soma = pontos.sum(1)

    pontos_aux[0] = pontos[np.argmin(soma)]  # [0,0]
    pontos_aux[3] = pontos[np.argmax(soma)]  # [w,h]
    subtracao = np.diff(pontos, axis=1)
    pontos_aux[1] = pontos[np.argmin(subtracao)]  # [w,0]
    pontos_aux[2] = pontos[np.argmax(subtracao)]  # [h,0]

    return pontos_aux


# Localiza o retangulo que contem 25 questoes conforme o modelo
# da folha de respostas.
# Esta funcao recebe como entrada os contornos da funcao do OpenCV
def localizaRetangulos(contornos):

    retangulo = []
    area_maxima = 0
    for i in contornos:
        area = cv2.contourArea(i)

        # se a area for maior que 50
        if area > 50:

            # calcula o perimetro
            perimetro = cv2.arcLength(i, True)

            # retorna o contorno desse perimetro
            contorno_perimetro = cv2.approxPolyDP(i, 0.02 * perimetro, True)
            if len(contorno_perimetro) == 4:
                retangulo.append(i)

    retangulo = sorted(retangulo, key=cv2.contourArea, reverse=True)

    return retangulo


# localiza os vertices dos retangulos para realizar o recorte de área
# com as questões
def localizaVertices(cont):

    # calcula o perimetro da figura
    # true indica que é o um contorno fechado
    perimetro = cv2.arcLength(cont, True)

    # realiza uma aproximacao da linha de contorno
    linha = cv2.approxPolyDP(cont, 0.02 * perimetro, True)
    return linha


# Quebra o bloco de questoes em 25 linha (1 linha por questao)
# e também cada questao em 5 colunas (5 alternativas)
def divideBlocoPorQuestao(imagem):

    questoes = []

    # quebra as questoes em 25 linhas
    linhas = np.vsplit(imagem, 25)

    # quebra cada uma das 25 linhas em 5 colunas(5 alternativas)
    for l in linhas:
        colunas = np.hsplit(l, 5)
        for alternativa in colunas:
            questoes.append(alternativa)
    return questoes
