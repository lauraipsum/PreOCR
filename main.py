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
        imagem_erosao = np.ones_like(imagem)  # Inicialmente, todos os pixels são definidos como brancos
        
        for i in range(1, altura):  # Começando de 1 para evitar o primeiro pixel da imagem
            for j in range(1, largura):  # Começando de 1 para evitar o primeiro pixel da linha
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
        imagem_dilatacao = np.zeros_like(imagem)  # Inicialmente, todos os pixels são definidos como pretos
        
        for i in range(altura - 1):  # Evitando a última linha da imagem
            for j in range(largura - 1):  # Evitando a última coluna da imagem
                if imagem[i, j] == 1 or imagem[i + 1, j] == 1 or imagem[i, j + 1] == 1:  
                    # Verifica se pelo menos um dos pixels adjacentes é preto (valor 1) na vertical ou horizontal
                    imagem_dilatacao[i, j] = 1
                    
        return imagem_dilatacao
    except Exception as e:
        print(f"Erro ao aplicar dilatação: {e}")
        return None

def aplicar_abertura(imagem):
    try:
        imagem_erosao = aplicar_erosao(imagem)

        imagem_abertura = aplicar_dilatacao(imagem_erosao)

        print("Abertura aplicada.")
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


def circunscritas_por_retangulo(imagem):
    altura, largura = imagem.shape
    imagem_circunscrita = np.copy(imagem)

    # Identifica as palavras na imagem
    palavras = []
    in_palavra = False
    for i in range(altura):
        for j in range(largura):
            if imagem[i, j] == 0:
                if not in_palavra:
                    palavras.append([(i, j)])
                    in_palavra = True
                else:
                    palavras[-1].append((i, j))
            else:
                if in_palavra:
                    if len(palavras[-1]) >=  15:  
                        in_palavra = False
                    else:
                        palavras.pop()

    # desenha retângulos ao redor de cada palavra
    for palavra in palavras:
        min_i = min(p[0] for p in palavra)
        max_i = max(p[0] for p in palavra)
        min_j = min(p[1] for p in palavra)
        max_j = max(p[1] for p in palavra)

        # Desenha o retângulo ao redor da palavra
        imagem_circunscrita[min_i-1:min_i+2, min_j-1:max_j+2] = 1
        imagem_circunscrita[max_i-1:max_i+2, min_j-1:max_j+2] = 1
        imagem_circunscrita[min_i-1:max_i+2, min_j-1:min_j+2] = 1
        imagem_circunscrita[min_i-1:max_i+2, max_j-1:max_j+2] = 1

    for i in range(len(palavras) - 1):
        min_i = min(p[0] for p in palavras[i])
        max_i = max(p[0] for p in palavras[i])
        min_j = min(p[1] for p in palavras[i])
        max_j = max(p[1] for p in palavras[i])

        next_min_i = min(p[0] for p in palavras[i+1])
        next_max_i = max(p[0] for p in palavras[i+1])

        if next_min_i - max_i >= 15:
            imagem_circunscrita[max_i+1:max_i+6, min_j-1:max_j+2] = 1
            imagem_circunscrita[next_min_i-6:next_min_i-1, min_j-1:max_j+2] = 1

    return imagem_circunscrita











def main():
    nome_arquivo_entrada = 'entrada.pbm'


    
    imagem = ler_imagem_pbm(nome_arquivo_entrada)
    salvar_imagem_pbm('saida.pbm', imagem)
    print(f"Imagem salva.")

    
    imagem_filtrada = aplicar_filtro_mediana(imagem, size=3) # mediana 3x3
    salvar_imagem_pbm('mediana.pbm', imagem_filtrada)
    print("Filtro da mediana aplicado.")

    
    # imagem_abertura = aplicar_abertura(imagem_filtrada) 
    # salvar_imagem_pbm('abertura.pbm', imagem_abertura)
    
    imagem_fechamento = aplicar_fechamento(imagem_filtrada) 
    salvar_imagem_pbm('fechamento.pbm', imagem_fechamento)
    print("Fechamento aplicado.")
    
    imagem_palavras_circunscritas = circunscritas_por_retangulo(imagem_fechamento)
    salvar_imagem_pbm('imagem_palavras_circunscritas.pbm', imagem_palavras_circunscritas)
    print("Imagem com palavras circunscritas salva.")

    


    

if __name__ == "__main__":
    main()
