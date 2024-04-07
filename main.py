import numpy as np

def ler_imagem_pbm(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as file:
            linhas = file.readlines()
            if not linhas[0].strip() == "P1":
                raise ValueError("Formato de arquivo inválido. Deve ser um arquivo PBM P1.")
            
            linhas = [linha.strip() for linha in linhas if not linha.startswith('#')] # remove comentários
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
        
        for i in range(1, altura):  # começando de 1 p/ evitar o primeiro pixel da imagem
            for j in range(1, largura):  # começando de 1 p/ evitar o primeiro pixel da linha
                if imagem[i, j] == 0 and imagem[i - 1, j] == 0 and imagem[i, j - 1] == 0:  
                    # Verifica se todos os pixels adjacentes na vertical e horizontal são pretos (valor 0)
                    imagem_erosao[i, j] = 0
                    
        return imagem_erosao
    except Exception as e:
        print(f"Erro ao aplicar erosão: {e}")
        return None


def aplicar_dilatacao(imagem):
    try:
        altura, largura = imagem.shape
        imagem_dilatacao = np.zeros_like(imagem)  # inicializa c/ todos os pixels definidos como pretos
        
        for i in range(altura - 1):  # evita a ultima linha da imagem
            for j in range(largura - 1):  # evita a ultima coluna da imagem
                if imagem[i, j] == 1 or imagem[i + 1, j] == 1 or imagem[i, j + 1] == 1:  
                    # verifica se pelo menos 1 dos pixels adjacentes e preto na vertical ou  na horizontal
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

def circunscritas_por_retangulo(imagem, margem=2):
    altura, largura = imagem.shape
    imagem_circunscrita = np.copy(imagem)  

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
        # Desenha retangulo
        imagem_circunscrita[min_i:max_i+1, min_j] = 1
        imagem_circunscrita[min_i:max_i+1, max_j] = 1
        imagem_circunscrita[min_i, min_j:max_j+1] = 1
        imagem_circunscrita[max_i, min_j:max_j+1] = 1

    return imagem_circunscrita

def encontrar_contorno(imagem, i, j):
    
    
    altura, largura = imagem.shape
    contorno = [(i, j)]
    imagem[i, j] = 2 # marca o pixel como visitado com um valor diferente de 1

    fila = [(i, j)]

    while fila:
        ni, nj = fila.pop(0)
        vizinhos = [(ni-1, nj), (ni+1, nj), (ni, nj-1), (ni, nj+1),
                    (ni-2, nj), (ni+2, nj), (ni, nj-2), (ni, nj+2),
                    (ni-3, nj), (ni+3, nj), (ni, nj-3), (ni, nj+3)]

        for vi, vj in vizinhos:
            if 0 <= vi < altura and 0 <= vj < largura and imagem[vi, vj] == 1:
                contorno.append((vi, vj))
                imagem[vi, vj] = 2  # marca o pixel como visitado com um valor diferente de 1
                fila.append((vi, vj))

    return contorno

# def contagem(imagem):


#     return num_linhas, num_palavras





def main():
    nome_arquivo_entrada = 'entrada.pbm'


    
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
    
    imagem_com_retangulos = circunscritas_por_retangulo(imagem_dilatada)
    salvar_imagem_pbm('com_retangulos.pbm', imagem_com_retangulos)
    print("Retângulos circunscritos aplicados.")
    
    #     # Contar o número de linhas e palavras
    # num_linhas, num_palavras = contagem(imagem_com_retangulos)
    # print(f"Número de linhas: {num_linhas}")
    # print(f"Número de palavras: {num_palavras}")


if __name__ == "__main__":
    main()
