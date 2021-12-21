import random
import os
import time

def main():
    QtdIndividuosGerados = 100
    objetosUsados = 20
    listaTempo = []
    
    while(objetosUsados <= 100):
        ini = time.time()
        print(objetosUsados)
        listaSolucoes = []
        listaMelhores = []
        novaGeracao = geraPopulacao(objetosUsados, QtdIndividuosGerados)
        xGeracoes, contaGeracoes, verificaMelhor = 20, 0, 0

        while(contaGeracoes < xGeracoes):

            novaGeracao, mel, listaMelhores = avaliacao(novaGeracao, objetosUsados, QtdIndividuosGerados)
            listaSolucoes = listaSolucoes + [mel]
            conta = 0

            if(verificaMelhor == 0):
                for i in range(50):
                    if(mel == listaMelhores[i][2]):
                        conta += 1
                    if(conta == 4): 
                        print('peso', listaMelhores[i][1], 'valor', listaMelhores[i][2])                      
                        verificaMelhor = 1
                        contaGeracoes = xGeracoes
                        break

            temMutacao = decisaoMutacao()

            if(temMutacao):
                mutacao(novaGeracao, QtdIndividuosGerados, objetosUsados)
    
            contaGeracoes += 1
        
        objetosUsados += 10
        fim = time.time()
        print(fim - ini)
       
        listaTempo = listaTempo + [(fim - ini)]


def objetos():
          # peso, valor
    obj = [ [50,898], [91,942], [97,13], [33,581], [99,621], [45,131], [51,405], [69,866], [39,788], [80,225],
            [72,348], [38, 756], [6,714], [79,159], [2,904], [23,223], [68,36], [88,243], [15,696], [75,837],
            [73,98], [7,985], [10,351], [10,744], [32,106], [4,731], [13,479], [64,475], [22,323], [26, 634],
            [26,937], [93,264], [44,731], [34,117], [21,268], [5,885], [88,534], [8,852], [7,155], [15,319],
            [92,909], [31,521], [2,430], [25,344], [61,801], [83,197], [48,308], [48,308], [9,733], [99,593],
            [91,121], [51,516], [58,761], [1,355], [53,579], [82,948], [82,330], [89,14], [55,179], [30,76],
            [78,543], [67,333], [47,655], [11,989], [75,84], [21,846], [59,925], [92,675], [38,59], [35,501],
            [59,806], [50,462], [36,503], [36,25], [58,924], [43,271], [62,688], [61,2], [50,284], [93,214],
            [33,385], [93,543], [44,102], [78,371], [64,115], [55,823], [49,430], [39,333], [58,923], [45,851],
            [4,352], [14,502], [97,381], [74,843], [48,191], [12,129], [86,96], [37,33], [73,878], [51,867]]
    
    return obj

def geraPopulacao(objetosUsados, quantidadeIndividuos):
    novaPop = []

    for i in range(quantidadeIndividuos):
        # determina o máximo de objetos a serem utilizados na resolução
        aleatorio = random.randrange(4, 7)

        novoIndividuo = []
        # inicializa todos os indivíduos com binário de objetos não utilizados (0)
        for iniciaInd in range(objetosUsados):
            novoIndividuo = novoIndividuo + [0]
            
        contador = 0

        # vai acessar todos os individuos
        for j in range(objetosUsados):

            # determina aleatoriamente o objeto a ser usado como possível resultado, caso val seja true
            val = bool(random.getrandbits(1))

            # caso val seja true
            if(val):
                contador += 1
                # verifica se a quantidade de objetos aleatórios estão dentro do limite a serem utilizados
                # para resolução
                if(contador <= aleatorio):
                    posicaoAleatoria = random.randrange(0, objetosUsados-1)
                    novoIndividuo[posicaoAleatoria] = 1
    
        # guarda o indivíduo na população
        novaPop = novaPop + [novoIndividuo]

    return novaPop

def avaliacao(novaGeracao, objetosUsados, quantidadeIndividuos):
    avaliacao = []

    avaliacao = calculaPesoVolume(quantidadeIndividuos, objetosUsados, novaGeracao)

    avaliacao = bubbleSortOrdena(quantidadeIndividuos, avaliacao)

    avaliacaoFinal = []
    avaliacaoFinal = solucoesOtimas(avaliacao, quantidadeIndividuos)
    guardaAvaliacao = []
    guardaAvaliacao = avaliacaoFinal

    melhorValor = avaliacaoFinal[0][2]
    contador = len(avaliacaoFinal)

    avaliacaoFinal = fitness(avaliacaoFinal, contador)

    novaGeracao = reproducao(novaGeracao, avaliacaoFinal, contador, objetosUsados)
    
    return novaGeracao, melhorValor, guardaAvaliacao
  
def calculaPesoVolume(quantidadeIndividuos, objetosUsados, novaGeracao):
    l = 0
    ob = objetos()
    avaliacao = []

    while(l < quantidadeIndividuos):
        posicao = []
        # verifica os objetos selecionados por aquele individuo
        for p in range(objetosUsados):
            if(novaGeracao[l][p] == 1):
                posicao = posicao + [p]

        t = len(posicao) # quantidade de objetos selecionados
        peso = 0
        volume = 0

        # função responsável por calcular o peso e o volume dos individuos
        for o in range(objetosUsados):
            for p in range(t):
                if(posicao[p] == o):
                    peso = peso + ob[o][0]
                    volume = volume + ob[o][1]

        l += 1
        soma = [l, peso, volume]
        avaliacao = avaliacao + [soma]
    
    return avaliacao

def bubbleSortOrdena(tamanho, lista): # função responsável por ordenar a lista conforme os pesos
    pVT = 1

    for pVT in range(tamanho):
        for pA in range(tamanho - 1):
            if(lista[pA][2] < lista[pA + 1][2]):# realiza a troca caso o valor da próxima 
                aux = lista[pA]                 # posição seja maior que o atual
                lista[pA] = lista[pA + 1]
                lista[pA + 1] = aux

    for pVT in range(tamanho):
        for pA in range(tamanho - 1):
            if(lista[pA][2] == lista[pA + 1][2]):# realiza a troca caso o peso da próxima 
                if(lista[pA][1] > lista[pA+1][1]): # peso seja igual ao atual
                    aux = lista[pA]                 
                    lista[pA] = lista[pA + 1]
                    lista[pA + 1] = aux

    return lista

def solucoesOtimas(lista, tamanho): # função que verifica os indivíduos da população que atendem ao
    capacidade = 250                # limite de peso
    listaSolucoes = []
    listaExcedentes = []
    listaFalta = []
    listaS = []
    contadorS = 0
    melhorSolucao = [] # pega a melhor solução dessa geração

    for i in range(tamanho):
        if(lista[i][1] <= capacidade): # verifica se o indivíduo atende ao peso ideal
            listaSolucoes = listaSolucoes + [lista[i]] # adiciona as possiveis soluções ótimas na lista

            if(contadorS == 0): melhorSolucao = melhorSolucao + [lista[i]]

            contadorS += 1

        else:
            listaExcedentes = listaExcedentes + [lista[i]]

    if(contadorS < 50): # caso os indivíduos ótimos fiquem abaixo dos 50%
        diferenca = 50 - contadorS
        
        for i in range(diferenca): # buscando alguns excedentes
            listaFalta = listaFalta + [listaExcedentes[i]]

        listaSolucoes = listaFalta + listaSolucoes
        listaSolucoes = bubbleSortOrdena(50, listaSolucoes)

    if(contadorS > 50): # caso haja excesso de possíveis soluções ótimas
        for i in range(40): # pegando os 40 melhores indivíduos
            listaS = listaS + [listaSolucoes[i]]

        j = contadorS - 10
        while(j < contadorS): # pegando os 10 piores indivíduos
            listaS = listaS + [listaSolucoes[j]]
            j += 1

        listaSolucoes = listaS

    return listaSolucoes

def fitness(lista, tamanho):
    valorPesoSorteio = tamanho
    pesoSorteio = []

    for i in range(tamanho): # define o peso de seleção de cada individuo que vai para reprodução
        pesoSorteio = pesoSorteio + [valorPesoSorteio]
        valorPesoSorteio -= 1
    
    for i in range(tamanho): # adiciona ao indíviduo o seu peso de seleção
        lista[i] = lista[i] + [pesoSorteio[i]]
        lista[i] = lista[i] + [i + 1]

    return lista        

def reproducao(geracao, lista, tamanho, objetosUsados):
    controle = 0
    temp = tamanho
    somaValorTotal = 0
    individuosNovaGeracao = []
    xCruzamentos = 0

    for i in range(tamanho): # calcula o valor total dos pesos de escolha dos indivíduos para a reprodução
        somaValorTotal = somaValorTotal + temp
        temp -= 1

    while(xCruzamentos < tamanho): # realiza os cruzamentos
        ind1, ind2 = [], []
        continua = 0
        pai, mae = 0, 0
        recebeSelecionado = 0

        while(continua < 2):
            controle = tamanho
            sorteiaIndividuo = random.randrange(1, somaValorTotal)
            #print('sorteado', sorteiaIndividuo)
        
            for i in range(tamanho): # seleciona os indivíduos que vão cruzar

                if(continua == 1): # evita a repetição de indivíduos
                    while(sorteiaIndividuo == recebeSelecionado):
                        sorteiaIndividuo = random.randrange(1, somaValorTotal)
        
                if(sorteiaIndividuo <= controle):
                   # print("individuo selecionado ",lista[i][0], "da posicao ", lista[i][4], '\n')
                    if(continua == 0):
                        pai = (lista[i][0] - 1)
                    elif(continua == 1):
                        mae = (lista[i][0] - 1)
              
                    recebeSelecionado = sorteiaIndividuo
                    continua += 1
                    break
                
                else:
                    controle = controle + (lista[i+1][3])

        selecionaGene = random.randrange(1, objetosUsados - 1) # seleciona a partir de que gene vai haver reprodução

        for i in range(objetosUsados): # realiza o cruzamento, gerando dois individuos
            if(i < selecionaGene):
                ind1 = ind1 + [geracao[pai][i]]
                ind2 = ind2 + [geracao[mae][i]]
            else:
                ind1 = ind1 + [geracao[mae][i]]
                ind2 = ind2 + [geracao[pai][i]]

        individuosNovaGeracao = individuosNovaGeracao + [ind1]
        individuosNovaGeracao = individuosNovaGeracao + [ind2]
 
        xCruzamentos += 1

    return individuosNovaGeracao

def decisaoMutacao(): # decide se vai haver ou não mutação

    decide = random.randrange(1, 100)
    if(decide <= 5):
        return True
    else:
        return False

def mutacao(novaGeracao, QtdIndividuosGerados, objetosUsados):

    decideQuemMuta = random.randrange(0, QtdIndividuosGerados - 1)
    decideQueGene = random.randrange(0, objetosUsados - 1)

    if(novaGeracao[decideQuemMuta][decideQueGene] == 1):
        novaGeracao[decideQuemMuta][decideQueGene] = 0      

    elif(novaGeracao[decideQuemMuta][decideQueGene] == 0):
        novaGeracao[decideQuemMuta][decideQueGene] = 1

main()
