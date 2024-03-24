def ler_imagem_pbm(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        
        linhas = [linha.strip() for linha in linhas if not linha.startswith('#')] # remove comentários

        if linhas[0] != 'P1':
            raise ValueError("Formato de arquivo inválido.") # exception pra caso n seja P1

        largura, altura = map(int, linhas[1].split())

        
        dados_pixel = []
        for linha in linhas[2:]:
            dados_pixel.extend([int(pixel) for pixel in linha.split()])

        return largura, altura, dados_pixel

def exibir_imagem(largura, altura, dados_pixel):
    for i in range(0, len(dados_pixel), largura):
        linha = dados_pixel[i:i+largura]
        print(' '.join(str(pixel) for pixel in linha))

def main():
    nome_arquivo = "Teste-20240324T210047Z-001\Teste\lorem_s12_c03.pbm"  # Insira o nome do arquivo aqui

    try:
        largura, altura, dados_pixel = ler_imagem_pbm(nome_arquivo)
        print("Largura:", largura)
        print("Altura:", altura)
        #print("PBM:")
        #exibir_imagem(largura, altura, dados_pixel)

    except ValueError as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()
