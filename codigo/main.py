from calculos_notas import calculaNota
import cv2
import numpy as np
import processamento as proc
import calculos_notas as nota

# path do gabarito
path_gabarito = "imagens/img01.jpg"
path_aluno = "imagens/img03.jpg"

# carrega imagem
imagem_gabarito = cv2.imread(path_gabarito)
imagem_aluno = cv2.imread(path_aluno)

# processa a imagem e transforma em um vetor
gabarito = proc.geraVetorResposta(imagem_gabarito)
aluno = proc.geraVetorResposta(imagem_aluno)

# calcula a nota, numero de acertos, erros, questoes acertadas, questoes erradas e questoes nulas
nota, acertos, erros, corretas, erradas, nulas = nota.calculaNota(
    gabarito, aluno)


print("A nota foi: ", nota)
print("Você errou", erros, " questões e acertou ", acertos, "questoes")
print("As questões erradas foram: ", erradas)
print("As questões corretas foram: ", corretas)
print("A prova teve as seguintes questões anuladas: ", nulas)
