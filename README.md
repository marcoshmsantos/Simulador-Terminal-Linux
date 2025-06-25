Simulador de Terminal Linux com B+Tree
Este projeto apresenta um simulador de um sistema de arquivos hierárquico, similar ao de terminais Linux, utilizando uma árvore B+ (B+Tree) como estrutura de dados subjacente para a indexação e gerenciamento de arquivos e diretórios.

Descrição
O objetivo principal deste trabalho é explorar a eficiência da estrutura de dados B+Tree na implementação de operações comuns de um sistema de arquivos. O simulador oferece uma interface de linha de comando (CLI) para interagir com o sistema, suportando comandos essenciais como mkdir, touch, ls, cd e rm.

Além da simulação, o projeto inclui:

Um script de benchmark para avaliar o desempenho das operações básicas e comparar os resultados práticos com a complexidade teórica esperada da B+Tree.
Um visualizador gráfico que renderiza a estrutura do sistema de arquivos em um canvas, oferecendo uma representação intuitiva da árvore de diretórios e arquivos.
Funcionalidades
Simulação de Comandos: Interface de linha de comando para manipulação do sistema de arquivos.
Estrutura de Dados Eficiente: Uso de uma B+Tree para garantir operações de busca, inserção e remoção com complexidade logarítmica (O(
log_bN)).
Comandos Suportados:
mkdir <nome_diretorio>: Cria um novo diretório.
touch <nome_arquivo>: Cria um novo arquivo vazio.
ls: Lista o conteúdo do diretório atual.
cd <caminho>: Navega para um diretório específico.
cd ..: Retorna ao diretório pai.
rm <nome>: Remove um arquivo ou diretório (e seu conteúdo).
Benchmark e Análise: Um script dedicado para testar o tempo de execução das operações e validar a eficiência da estrutura de dados.
Visualizador Gráfico: Uma ferramenta que desenha a árvore do sistema de arquivos em um canvas para fácil compreensão da hierarquia.
