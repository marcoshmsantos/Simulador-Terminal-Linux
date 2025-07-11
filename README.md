# Simulador de Terminal Linux com B+Tree
Este projeto apresenta um simulador de um sistema de arquivos hierárquico, similar ao de terminais Linux, utilizando uma árvore B+Tree como estrutura de dados principal para a indexação e gerenciamento de arquivos e diretórios.

# Descrição
O objetivo principal deste trabalho é explorar a eficiência da estrutura de dados B+Tree na implementação de operações comuns de um sistema de arquivos. O simulador oferece uma interface de linha de comando para interagir com o sistema, suportando comandos essenciais como mkdir, touch, ls, cd e rm.

Além da simulação, o projeto inclui:

1. Um script de benchmark para avaliar o desempenho das operações básicas e comparar os resultados práticos com a complexidade teórica esperada da B+Tree.
2. Um visualizador gráfico que renderiza a estrutura do sistema de arquivos em um canvas, oferecendo uma representação intuitiva da árvore de diretórios e arquivos.
# Funcionalidades
Simulação de comandos: interface de linha de comando para manipulação do sistema de arquivos.
Estrutura de dados eficiente: uso de uma B+Tree para garantir operações de busca, inserção e remoção com complexidade logarítmica.
# Comandos Suportados:
- mkdir <nome_diretorio>: cria um novo diretório.
- touch <nome_arquivo>: cria um novo arquivo vazio.
- ls: lista o conteúdo do diretório atual.
- cd <caminho>: navega para um diretório específico.
- cd ..: retorna ao diretório pai.
- rm <nome>: remove um arquivo ou diretório vazio.
