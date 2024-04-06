import numpy as np
from PIL import Image
from scipy.ndimage import median_filter

def ler_imagem_pbm(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        
        linhas = file.readlines()
        linhas = [linha.strip() for linha in linhas if not linha.startswith('#')] # remove coment

        largura, altura = map(int, linhas[1].split())
        
        dados = ''.join(linhas[2:])

        
        imagem = np.array([int(bit) for bit in dados if bit.isdigit()]) # converte os dados p/ uma lista de inteiros
        
        # redimensiona a imagem para a forma correta
        imagem = imagem.reshape(altura, largura)
        
        return imagem

def salvar_imagem_pbm(nome_arquivo, imagem):
    with open(nome_arquivo, 'w') as file:
        file.write("P1\n") #cabecalho da nova imagem
        file.write("# Nova imagem\n")
        file.write(f"{imagem.shape[1]} {imagem.shape[0]}\n")
        
       
        for linha in imagem:
            file.write(" ".join(map(str, linha)) + "\n")

def aplicar_filtro_mediana(imagem, size):
    altura, largura = imagem.shape
    imagem_filtrada = np.zeros_like(imagem) #matriz de zeros pra inicializar
    
    
    for i in range(altura):
        for j in range(largura):
            
            vizinhanca = imagem[ #mediana da vizinhança do pixel atual
                max(0, i - size // 2):min(altura, i + size // 2 + 1),
                max(0, j - size // 2):min(largura, j + size // 2 + 1)]
             
            imagem_filtrada[i, j] = np.median(vizinhanca)
    
    return imagem_filtrada

def main():
    nome_arquivo_entrada = 'entrada.pbm'
    nome_arquivo_saida = 'saida.pbm'
    nome_arquivo_mediana = 'mediana.pbm'
    
    imagem = ler_imagem_pbm(nome_arquivo_entrada)
    salvar_imagem_pbm(nome_arquivo_saida, imagem)
    
    imagem_filtrada = aplicar_filtro_mediana(imagem,size=3) #mediana 3x3
    salvar_imagem_pbm(nome_arquivo_mediana, imagem_filtrada)

if __name__ == "__main__":
    main()
