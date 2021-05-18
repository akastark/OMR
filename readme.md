# Optical Mark Recognition

Olá! Este é um projeto implementado em Python como trabalho da disciplina de Processamento Digital de Imagens do curso de Engenharia de Computação.

O projeto consiste em um algoritmo de Optical Mark Recognition, método de reconhecimento de marcas em imagens, no caso deste projeto aplicado na correção automática de provas.

# Arquivos

Abaixo temos os arquivos que este repositório contém.

## Pasta código

Esta pasta contém 4 arquivos:
**codigo/preprocessamento.py** que realiza o pré processamento da imagem (escala de cinza, Canny e Gaussian Blur). //
**codigo/processamento.py**  funções que realizam as manipulações e segmentações de imagem para aplicação do OMR. // 
**codigo/calculos_notas.py**  processo que realiza o cálculo da nota com base na comparação com um gabarito. //
**codigo/main.py**  chamadas da funções principais. //

## folha_respostas.pdf

Modelo de folha de respostas utilizado.
## especificacoes_projeto.pdf

Arquivo com as especificações do projeto requeridas pelo professor.

## relatório.pdf

Artigo descrevendo todo o funcionamento do algoritmo e também um referencial teórico.

## apresentacao

Apresentacao em PDF para a disciplina

# Bibliotecas necessárias

Este projeto utiliza NumPy e OpenCV.
Para instalar usando Pip rode os seguintes comandos.

    pip install opencv2
    pip install numpy

## Utilização

Preencha e digitalize uma folha respostas e coloca na pasta imagens/. Para rodar passe o nome da imagem para a variável sinalizada no arquivo *main.py*

Utilize o comando `python main.py` para executar.

A saída será algo como:

    A nota foi:  100.0
    Você errou 0  questões e acertou  50 questoes
    As questões erradas foram:  []
    As questões corretas foram:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
