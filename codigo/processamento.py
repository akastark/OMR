#########################################################
#  ARQUIVO COM O CODIGO DE PROCESSAMENTO DAS QUESTOES   #
#########################################################

import cv2
import numpy as np
import preprocessamento as pre
import processamento as proc

# reordena os pontos dos vertices em ordem crescente do contorno


def ordenaPontosVertice(pontos):

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


# Processa as questões e salva num vetor a resposta equivalente
# A=0, B=1 ....
def processaQuestoes(retangulo):
    pixels = np.zeros((25, 5))
    coluna = 0  # alternativa
    linha = 0  # questao

    for questao in retangulo:

        # conta o numero de pixels não nulos no corte da alternativa
        total_pixels = cv2.countNonZero(questao)
        pixels[linha][coluna] = total_pixels

        coluna += 1
        if coluna == 5:
            linha += 1
            coluna = 0

    # vetor de respostas
    respostas = []

    for x in range(0, 25):
        aux = pixels[x]

        # verifica se questao possui alternativa assinalada
        # caso a qtde de pixels nao nulos seja menor que 1200 nao possui alternativa assinalada
        limite_minimo = np.amin(aux)*1.5
        if(np.amax(aux) > limite_minimo):

            alternativa_assinalada = np.where(aux == np.amax(aux))

            # ordena para localizar a segunda maior
            aux.sort()

            # compara as duas maiores alternativas, se a segunda maior tiver 80% do valor da proxima
            # considera como duas questoes assinaladas e anula a questao
            if((aux[3]/np.amax(aux)) > 0.8):
                alternativa_assinalada[0][0] = -2

        else:
            alternativa_assinalada[0][0] = -1

        respostas.append(alternativa_assinalada[0][0])

    return respostas


# processa o retangulo fazendo a leitura das questoes
def processaRetantagulo(retangulo, imagem_original, largura, altura):

    if retangulo.size != 0:

        # reordena os pontos do retangulo
        retangulo = proc.ordenaPontosVertice(retangulo)

        # pontos da matriz de transformação para  o retangulo
        pt1 = np.float32(retangulo)
        pt2 = np.float32(
            [[0, 0], [largura, 0], [0, altura], [largura, altura]])

        # cria matriz de transformação do retangulo esquerdo
        matriz = cv2.getPerspectiveTransform(pt1, pt2)

        # aplica transformacao nos retangulos
        retangulo_warp = cv2.warpPerspective(
            imagem_original, matriz, (largura, altura))

        # APLICA O THRESHOLD
        retangulo_warp_gray = cv2.cvtColor(
            retangulo_warp, cv2.COLOR_BGR2GRAY)

        retangulo_thresh = cv2.threshold(
            retangulo_warp_gray, 150, 255, cv2.THRESH_BINARY_INV)[1]

        questoes = divideBlocoPorQuestao(retangulo_thresh)

        return questoes


# processa a imagem e faz a leitura das alternativas salvando em um vetor
def geraVetorResposta(imagem):

    largura = 800
    altura = 1200

    imagem = cv2.resize(imagem, (largura, altura))

    imagem_processada = pre.preProcessamento(imagem)

    # procura os contornos na imagem
    contornos, hierarquia = cv2.findContours(
        imagem_processada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #contorno = imagem.copy()

    # procura retangulo
    retangulos = proc.localizaRetangulos(contornos)

    # cv2.drawContours(contorno, contornos, -1, (0, 255, 0), 1)
    # cv2.imshow("teste", contorno)
    # cv2.waitKey(0)

    retangulo_esquerdo = localizaVertices(retangulos[0])  # questoes 1 a 25
    retangulo_direito = localizaVertices(retangulos[1])  # questoes 26 a 50

    # questoes do lado esquerdo
    questoes_esquerdo = processaRetantagulo(
        retangulo_esquerdo, imagem, largura, altura)

    # questos do lado direito
    questoes_direito = processaRetantagulo(
        retangulo_direito, imagem, largura, altura)

    # concatena os dois retangulos de respostas
    respostas = processaQuestoes(
        questoes_esquerdo) + processaQuestoes(questoes_direito)

    print("Respostas:", respostas)
    return respostas
