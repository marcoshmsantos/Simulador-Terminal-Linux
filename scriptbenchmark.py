import time
import math
import random
import matplotlib.pyplot as plt
from BPlustree import BplusTree
ordem=16
def benchmark_bplustree():
    #tamanhos de entrada 
    entradas = [10000, 10000, 100000]

    #lista para armazenar os tempo
    tempo_inserção = []
    tempo_busca = []
    tempo_deleção = []

    #executa os testes para todos os tamanhos de entrada
    for entrada in entradas:

        #teste de inserção
        tree = BplusTree(ordem)
        dados = [(i, f"chave_{i}") for i in range(entrada)]
        random.shuffle(dados)  
        tempo_início = time.perf_counter()
        for valor, chave in dados:
            tree.inserção(valor, chave) 
        inserção = time.perf_counter() - tempo_início
        tempo_inserção.append(inserção)

        #teste de busca, trabalha com 25% dos dados inseridos
        n = entrada//4
        valor_busca = random.sample([str(i) for i in range(entrada)], min(n, entrada))
        tempo_início = time.perf_counter()
        for valor in valor_busca:
            tree.busca(valor)  
        busca = time.perf_counter() - tempo_início
        tempo_busca.append(busca)

        #teste de remoção, trabalha com 25% dos dados inseridos
        deleção_candidatos = random.sample(dados, n)
        deleções_corretas = 0
        tempo_início = time.perf_counter()
        
        for valor, chave in deleção_candidatos:
            if tree.verifica_existência(str(valor), chave):  
                try:
                    tree.delete(str(valor), chave) 
                    deleções_corretas += 1
                except Exception as e:
                    continue
        deleção = time.perf_counter() - tempo_início
        tempo_deleção.append(deleção)
    return entradas, tempo_inserção, tempo_busca, tempo_deleção

#calcula a complexidade teórica esperada para uma bplustree de ordem m, levando em conta a quantidade de operações
def calculadora_complexidade(entradas, ordem, operação):
    valor_complexidade = []
    for n in entradas:
        if n <= 1:
            valor_complexidade.append(1)
            continue
        log_m_n = math.log(n) / math.log(ordem)
        if operação == 'insert':
            complexidade = n * log_m_n
        else:
            k = n//4
            complexidade = k * log_m_n
        valor_complexidade.append(complexidade)
    return valor_complexidade

#plota os gráficos de cada operação, o tempo necessário para certa quantidade de elementos
def plot_performance(entradas, tempo_inserção , tempo_busca, tempo_deleção, ordem):

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Benchmark B+ Tree (Ordem/m = {ordem})', fontsize=16)
    
    inserção_complexidade = calculadora_complexidade(entradas, ordem, 'insert')
    busca_complexidade = calculadora_complexidade(entradas, ordem, 'search')  
    deleção_complexidade = calculadora_complexidade(entradas, ordem, 'delecao')  
    
    def ajuste(tempo_real, tempo_teórico):
        if len(tempo_real) < 2 or any(t <= 0 for t in tempo_teórico):
            return tempo_teórico
        pares_válidos = [(r, t) for r, t in zip(tempo_real, tempo_teórico) if r > 0 and t > 0]
        if len(pares_válidos) >= 2:
            fator_de_escala = [r/t for r, t in pares_válidos[:2]]
            escala = sum(fator_de_escala) / len(fator_de_escala)
        else:
            escala = tempo_real[0] / tempo_teórico[0] if tempo_teórico[0] > 0 else 1
        return [t * escala for t in tempo_teórico]
    inserção_teórica = ajuste(tempo_inserção, inserção_complexidade)
    busca_teórica = ajuste(tempo_busca, busca_complexidade)
    deleção_teórica = ajuste(tempo_deleção, deleção_complexidade)

    axes[0, 0].plot(entradas, tempo_inserção, 'bo-', label='Tempo Real', linewidth=2, markersize=6)
    axes[0, 0].plot(entradas, inserção_teórica, 'y--', label='Curva Teórica O(n⋅log_m(n))', linewidth=2)
    axes[0, 0].set_xlabel('Número de Elementos (n)')
    axes[0, 0].set_ylabel('Tempo Total (s)')
    axes[0, 0].set_title('Performance de Inserção')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(entradas, tempo_busca, 'go-', label='Tempo Real', linewidth=2, markersize=6)
    axes[0, 1].plot(entradas, busca_teórica, 'y--', label='Curva Teórica O(k⋅log_m(n))', linewidth=2)
    axes[0, 1].set_xlabel('Número de Elementos (n)')
    axes[0, 1].set_ylabel('Tempo Total (s)')
    axes[0, 1].set_title('Performance de Busca (25% dos elementos)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].plot(entradas, tempo_deleção, 'ro-', label='Tempo Real', linewidth=2, markersize=6)
    axes[1, 0].plot(entradas,deleção_teórica, 'y--', label='Curva Teórica O(k⋅log_m(n))', linewidth=2)
    axes[1, 0].set_xlabel('Número de Elementos (n)')
    axes[1, 0].set_ylabel('Tempo Total (s)')
    axes[1, 0].set_title('Performance de Remoção (25% dos elementos)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].plot(entradas, tempo_inserção, 'bo-', label='Inserção', linewidth=2, markersize=4)
    axes[1, 1].plot(entradas, tempo_busca, 'go-', label='Busca', linewidth=2, markersize=4)  
    axes[1, 1].plot(entradas, tempo_deleção, 'mo-', label='Remoção', linewidth=2, markersize=4)
    axes[1, 1].set_xlabel('Número de Elementos (n)')
    axes[1, 1].set_ylabel('Tempo Total (s)')
    axes[1, 1].set_title('Comparação das Operações')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    entradas, tempo_inserção, tempo_busca, tempo_deleção = benchmark_bplustree()
    plot_performance(entradas, tempo_inserção, tempo_busca, tempo_deleção, ordem)
    