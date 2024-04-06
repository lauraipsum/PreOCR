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
        imagem_erosao = np.zeros_like(imagem)  # Inicialmente, todos os pixels são definidos como pretos
        
        for i in range(1, altura):  # Evita o primeiro pixel da imagem
            for j in range(1, largura):  # Evita o primeiro pixel da linha
                if imagem[i, j] == 1 and imagem[i - 1, j] == 1 and imagem[i, j - 1] == 1:  
                    # Verifica se todos os pixels adjacentes na vertical e horizontal são pretos (valor 1)
                    imagem_erosao[i, j] = 1
                    
        return imagem_erosao
    except Exception as e:
        print(f"Erro ao aplicar erosão: {e}")
        return None



def aplicar_dilatacao(imagem):
    try:
        altura, largura = imagem.shape
        imagem_dilatacao = np.zeros_like(imagem)  
        
        for i in range(altura - 1):  # evitra a última linha 
            for j in range(largura - 1):  # evita a ultima coluna 
                if imagem[i, j] == 1 or imagem[i + 1, j] == 1 or imagem[i, j + 1] == 1:  
                    # verifica se pelo menos 1 dos pixels adjacentes e preto (valor 1) na vertical ou horizontal
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

def main():
    nome_arquivo_entrada = 'entrada.pbm'
    nome_arquivo_saida = 'saida.pbm'
    nome_arquivo_mediana = 'mediana.pbm'
    nome_arquivo_abertura = 'abertura.pbm'
    nome_arquivo_fechamento = 'fechamento.pbm'
    nome_arquivo_dilatacao = 'dilatacao.pbm'



    
    imagem = ler_imagem_pbm(nome_arquivo_entrada)
    salvar_imagem_pbm(nome_arquivo_saida, imagem)
    print(f"Imagem salva.")

    
    imagem_filtrada = aplicar_filtro_mediana(imagem, size=3) # mediana 3x3
    salvar_imagem_pbm(nome_arquivo_mediana, imagem_filtrada)
    print("Filtro da mediana aplicado.")

    
    # imagem_abertura = aplicar_abertura(imagem_filtrada) 
    # salvar_imagem_pbm(nome_arquivo_abertura, imagem_abertura)
    # print("Abertura aplicada.")
    
    imagem_dilatada = aplicar_dilatacao(imagem_filtrada)
    salvar_imagem_pbm(nome_arquivo_dilatacao, imagem_dilatada)
    print("Dilatacao aplicada.")

    imagem_fechamento = aplicar_fechamento(imagem_dilatada) 
    salvar_imagem_pbm(nome_arquivo_fechamento, imagem_fechamento)
    print("Fechamento aplicado.")

    


    

if __name__ == "__main__":
    main()
