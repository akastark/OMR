#########################################################
#  ARQUIVO COM O CODIGO DE CALCULO DA NOTA              #
#########################################################


# calcula a nota comparando o gabarito com as respostas do aluno
# caso o gabarito nao tenha questao preenchida, calcula a nota em cima das questoes validas
# caso o aluno nao tenha preenchido, zera a questao


from numpy.lib.function_base import append


def calculaNota(gabarito, respostas):

    if len(gabarito) != len(respostas):
        print("Erro: os vetores resposta e gabarito possuem tamanhos diferentes")
        return 300

    qtd_corretas = 0
    corretas = []

    qtd_erradas = 0
    erradas = []

    qtd_questoes_validas_gabarito = 50
    nulas = []
    marcas_duplas = []

    index = 1

    for i in range(0, 50):

        # se a resposta for igual a do gabarito
        if respostas[i] == gabarito[i] and gabarito[i] != -1:
            qtd_corretas += 1
            corretas.append(index)

        # se o gabarito nao estiver assinalado naquela i
        elif respostas[i] != gabarito[i]:
            if gabarito[i] == -1:
                qtd_questoes_validas_gabarito -= 1
                nulas.append(index)

            elif gabarito[i] == -2:
                qtd_questoes_validas_gabarito -= 1
                nulas.append(index)

            elif respostas[i] == -2:
                qtd_erradas += 1
                marcas_duplas.append(index)

            else:
                qtd_erradas += 1
                erradas.append(index)

        index += 1
    # calcula a nota do aluno
    nota = (qtd_corretas/qtd_questoes_validas_gabarito) * 100

    return nota, qtd_corretas, qtd_erradas, corretas, erradas, nulas, marcas_duplas
