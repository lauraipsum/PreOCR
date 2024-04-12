Objetivo: Processar uma imagem binária, no formato PBM ASCII (PGM tipo P1), que contém um texto com uma ou mais
colunas. Como saída, o programa retorna quantas linhas e palavras esse texto contém, e gera uma imagem PBM contendo o texto da entrada, porém com cada palavra do texto circunscrita por um retângulo. 

## Modo de uso:

Primeiramente, é necessário instalar a biblioteca NumPy

    pip install numpy
    
No arquivo **main.py**:

Modifique o valor da variável  **nome_arquivo_entrada** para o caminho do .pbm que deseja selecionar.

Por fim, basta executar o arquivo **main.py**

## Funções:

**`ler_imagem_pbm(nome_arquivo)`:** Recebe o nome de um arquivo no formato PBM e lê sua estrutura. Ela verifica se o arquivo está no formato correto (P1) e extrai as informações sobre a largura, altura e dados da imagem, retornando uma matriz NumPy representando a imagem.
    
**`salvar_imagem_pbm(nome_arquivo, imagem)`:** Salva uma matriz de imagem em um arquivo no formato PBM. Ela escreve o cabeçalho do arquivo e os dados da imagem.
    
**`aplicar_filtro_mediana(imagem, size)`:** Aplica um filtro de mediana à imagem. Para cada pixel da imagem, ela calcula a mediana dos valores dos pixels em uma vizinhança de tamanho `size` ao redor desse pixel e substitui o valor do pixel pela mediana calculada.
    
**`aplicar_erosao(imagem)`:** Aplica o operador de erosão à imagem.
    
 **`aplicar_dilatacao(imagem)`:** Essa função aplica o operador de dilatação à imagem. 
    
**`aplicar_abertura(imagem)`:** Aplica uma abertura morfológica à imagem, que consiste em primeiro aplicar a erosão e depois a dilatação.
    
 **`aplicar_fechamento(imagem)`:** Aplica um fechamento morfológico à imagem, que consiste em primeiro aplicar a dilatação e depois a erosão.
    
**`circunscritas_por_retangulo(imagem, margem=1)`:** Identifica as regiões de interesse na imagem (palavras) e desenha retângulos ao redor delas.
    
**`contagem_palavras(imagem)`:** Conta o número de palavras na imagem, com base nas regiões identificadas anteriormente.
    
  **`contagem_linhas(coordenadas_retangulos)`:** Conta o número de linhas na imagem, usando as coordenadas dos retângulos que circunscrevem as palavras.
