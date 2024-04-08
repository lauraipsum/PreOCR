import numpy as np
import time

def ler_imagem_pbm(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as file:
            linhas = file.readlines()
            if not linhas[0].strip() == "P1":
                raise ValueError("Formato de arquivo inválido. Deve ser um arquivo PBM P1.")
            
            linhas = [linha.strip() for linha in linhas if not linha.startswith('#')] # remove comentarios
            largura, altura = map(int, linhas[1].split())
            dados = ''.join(linhas[2:])
            
            imagem = np.array([int(bit) for bit in dados if bit.isdigit()]) # converte os dados para uma lista de inteiros
            imagem = imagem.reshape(altura, largura)
            
            return imagem
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Erro: {e}")
        return None

def salvar_imagem_pbm(nome_arquivo, imagem):
    try:
        with open(nome_arquivo, 'w') as file:
            file.write("P1\n") # cabeçalho da nova imagem
            file.write("# Nova imagem\n")
            file.write(f"{imagem.shape[1]} {imagem.shape[0]}\n")
            
            for linha in imagem:
                file.write(" ".join(map(str, linha)) + "\n")
                
    except Exception as e:
        print(f"Erro ao salvar imagem: {e}")

def aplicar_filtro_mediana(imagem, size):
    try:
        altura, largura = imagem.shape
        imagem_filtrada = np.zeros_like(imagem) # matriz de zeros para inicializar
        
        for i in range(altura):
            for j in range(largura):
                vizinhanca = imagem[ # mediana da vizinhança do pixel atual
                    max(0, i - size // 2):min(altura, i + size // 2 + 1),
                    max(0, j - size // 2):min(largura, j + size // 2 + 1)]
                imagem_filtrada[i, j] = np.median(vizinhanca)
                
        return imagem_filtrada
    except Exception as e:
        print(f"Erro ao aplicar filtro da mediana: {e}")
        return None

def aplicar_erosao(imagem):
    try:
        altura, largura = imagem.shape
        imagem_erosao = np.ones_like(imagem)  # inicializa c/ todos os pixels definidos como brancos
        
        for i in range(altura):  # começando de 0 para cobrir toda a imagem
            for j in range(largura):  # começando de 0 para cobrir toda a linha
                if imagem[i, j] == 0 and (i == 0 or imagem[i - 1, j] == 0) and (j == 0 or imagem[i, j - 1] == 0):  
                    # verifica se todos os pixels adjacentes na vertical e horizontal são pretos (valor 0)
                    imagem_erosao[i, j] = 0
                    
        return imagem_erosao
    except Exception as e:
        print(f"Erro ao aplicar erosão: {e}")
        return None

def aplicar_dilatacao(imagem):
    try:
        altura, largura = imagem.shape
        imagem_dilatacao = np.zeros_like(imagem)  # inicializa c/ todos os pixels definidos como pretos
        
        for i in range(altura):  
            for j in range(largura):  
                if imagem[i, j] == 1 or (i < altura - 1 and imagem[i + 1, j] == 1) or (j < largura - 1 and imagem[i, j + 1] == 1):  
                    # verifica se pelo menos 1 dos pixels adjacentes é preto na vertical ou na horizontal
                    imagem_dilatacao[i, j] = 1
                    
        return imagem_dilatacao
    except Exception as e:
        print(f"Erro ao aplicar dilatação: {e}")
        return None




def aplicar_abertura(imagem):
    try:
        imagem_erosao = aplicar_erosao(imagem)

        imagem_abertura = aplicar_dilatacao(imagem_erosao)

        return imagem_abertura
    except Exception as e:
        print(f"Erro ao aplicar abertura: {e}")
        return None
    
def aplicar_fechamento(imagem):
        try:
            imagem_dilatacao = aplicar_dilatacao(imagem)
            imagem_fechamento = aplicar_erosao(imagem_dilatacao)

            return imagem_fechamento
        except Exception as e:
            print(f"Erro ao aplicar fechamento: {e}")
            return None

def circunscritas_por_retangulo(imagem, margem=1):
    altura, largura = imagem.shape
    imagem_circunscrita = np.copy(imagem)
    coordenadas_retangulos = []

    # contornos das palavras
    contornos = []
    for i in range(altura):
        for j in range(largura):
            if imagem[i, j] == 1:  # pixel preto encontrado
                contornos.append(encontrar_contorno(imagem, i, j))

    # desenha retangulo ao redor de cada palavra
    for contorno in contornos:
        min_i, min_j = np.maximum(np.min(contorno, axis=0) - margem, 0)
        max_i, max_j = np.minimum(np.max(contorno, axis=0) + margem, [altura - 1, largura - 1])
        coordenadas_retangulos.append(((min_i, min_j), (min_i, max_j), (max_i, min_j), (max_i, max_j)))  # coordenadas dos extremos

        # desenha o retangulo
        imagem_circunscrita[min_i:max_i+1, min_j] = 1
        imagem_circunscrita[min_i:max_i+1, max_j] = 1
        imagem_circunscrita[min_i, min_j:max_j+1] = 1
        imagem_circunscrita[max_i, min_j:max_j+1] = 1

    return imagem_circunscrita, coordenadas_retangulos

def encontrar_contorno(imagem, i, j):
    
    
    altura, largura = imagem.shape
    contorno = [(i, j)]
    imagem[i, j] = 2 # marca o pixel como visitado com um valor diferente de 1

    fila = [(i, j)]

    while fila:
        ni, nj = fila.pop(0)
        vizinhos = [(ni-1, nj), (ni+1, nj), (ni, nj-1), (ni, nj+1),
                    (ni-2, nj), (ni+2, nj), (ni, nj-2), (ni, nj+2),
                    (ni-3, nj), (ni+3, nj), (ni, nj-3), (ni, nj+3),
                    (ni-4, nj), (ni+4, nj), (ni, nj-4), (ni, nj+4),
                    (ni-5, nj), (ni+5, nj), (ni, nj-5), (ni, nj+5)]

        for vi, vj in vizinhos:
            if 0 <= vi < altura and 0 <= vj < largura and imagem[vi, vj] == 1:
                contorno.append((vi, vj))
                imagem[vi, vj] = 2  # marca o pixel como visitado com um valor diferente de 1
                fila.append((vi, vj))

    return contorno



def contagem_palavras(imagem):
    altura, largura = imagem.shape
    num_retangulos = 0
    imagem_temp = np.copy(imagem)

    for i in range(altura):
        for j in range(largura):
            if imagem_temp[i, j] == 1:  # encontra um pixel preto não visitado
                contorno = encontrar_retangulo(imagem_temp, i, j)
                if contorno is not None:  # se encontrar um retangulo
                    num_retangulos += 1
                    for pixel in contorno:
                        imagem_temp[pixel[0], pixel[1]] = 2  # marca os pixels do retangulo como visitados

    return num_retangulos

def encontrar_retangulo(imagem, i, j):
    altura, largura = imagem.shape
    retangulo = []

    fila = [(i, j)]
    while fila:
        ni, nj = fila.pop(0)
        if imagem[ni, nj] == 1:  
            retangulo.append((ni, nj))
            imagem[ni, nj] = 2  # marca como visitado
            # adiciona vizinhos que n foram visitados ainda
            vizinhos = [(ni-1, nj), (ni+1, nj), (ni, nj-1), (ni, nj+1)]
            for vi, vj in vizinhos:
                if 0 <= vi < altura and 0 <= vj < largura and imagem[vi, vj] == 1:
                    fila.append((vi, vj))

    # verifica se o contorno encontrado e um retangulo valido
    min_i, min_j = np.min(retangulo, axis=0)
    max_i, max_j = np.max(retangulo, axis=0)
    if max_i - min_i < 1 or max_j - min_j < 1:
        return None  #retangulo invalido
    return retangulo


def contagem_linhas(coordenadas_retangulos):
    num_linhas = 0
    max_y = -1  # valor inicial pra determinar a linha atual

    # ordenar coordenadas_retangulos pelo valor de y do ponto mais baixo de cada retângulo
    coordenadas_retangulos.sort(key=lambda coords: max(coords, key=lambda coord: coord[0])[0])

    for coords in coordenadas_retangulos:
        min_y = min(coords, key=lambda coord: coord[0])[0]
        if min_y > max_y:  # se a parte superior do retângulo está em uma nova linha
            num_linhas += 1
            max_y = max(coords, key=lambda coord: coord[0])[0]

    return num_linhas




def main():
    start_time = time.time()

    nome_arquivo_entrada = 'lorem_s12_c02_espacos_noise.pbm'


    
    imagem = ler_imagem_pbm(nome_arquivo_entrada)
    salvar_imagem_pbm('saida.pbm', imagem)
    print(f"Imagem salva.")

    
    imagem_filtrada = aplicar_filtro_mediana(imagem, size=3) # mediana 3x3
    salvar_imagem_pbm('mediana.pbm', imagem_filtrada)
    print("Filtro da mediana aplicado.")

    
    imagem_abertura = aplicar_abertura(imagem_filtrada) 
    salvar_imagem_pbm('abertura.pbm', imagem_abertura)
    print("Abertura aplicada.")

    
    # imagem_fechamento = aplicar_fechamento(imagem_filtrada) 
    # salvar_imagem_pbm('fechamento.pbm', imagem_fechamento)
    # print("Fechamento aplicado.")
    
    imagem_dilatada = aplicar_dilatacao(imagem_abertura)
    salvar_imagem_pbm('dilatacao.pbm', imagem_dilatada)
    print("Dilatacao aplicada")
    
    imagem_com_retangulos, coordenadas_retangulos = circunscritas_por_retangulo(imagem_dilatada)
    salvar_imagem_pbm('com_retangulos.pbm', imagem_com_retangulos)
    print("Retangulos circunscritos aplicados.")
    
    # # coordenadas dos retangulos
    # for i, coords in enumerate(coordenadas_retangulos):
    #     print(f"Retangulo {i+1}:")
    #     for coord in coords:
    #         print(coord)

    # contar o número de linhas e palavras
    num_palavras = len(coordenadas_retangulos)
    print(f"Número de palavras: {num_palavras}")
    
    
    num_linhas = contagem_linhas(coordenadas_retangulos)
    print(f"Número de linhas: {num_linhas}")
    
    end_time = time.time()

    execution_time = end_time - start_time

    print(f"Tempo total de execução: {execution_time} segundos")


if __name__ == "__main__":
    main()
