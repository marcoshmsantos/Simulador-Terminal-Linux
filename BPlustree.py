# B+ tee in python
import time
import math

class Node:
    def __init__(self, order):
        self.order = order #define a ordem da árvore
        self.values = [] #lista com os valores de cada nó
        self.keys = [] #lista com as chaves que correspondem a cada valor
        self.nextKey = None #ponteiro para o proximo nó
        self.parent = None #indica o nó pai, auxilia na divisão de nós
        self.check_leaf = False #diz se o nó é folha ou nó interno

    def insert_at_leaf(self, leaf, value, key): #insere um par valor-chave em uma folha
        if (self.values): #se o nó ja tem valores.
            lista_de_valores = self.values
            for i in range(len(lista_de_valores)):
                if (value == lista_de_valores[i]): #se o valor ja existe, adiciona a chave a lista de chaves 
                    self.keys[i].append(key)
                    break
                elif (value < lista_de_valores[i]): #se o valor é menor, insere na posição correta 
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif (i + 1 == len(lista_de_valores)): #se o valor é maior, insere no final
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else: #se o nó esta vazio, inicia a lista com os valores
            self.values = [value]
            self.keys = [[key]]


# B plus tree
class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.check_leaf = True

    # Insert operation
    def insert(self, value, key): #realiza a insercao
        value = str(value)
        old_node = self.search(value)
        old_node.insert_at_leaf(old_node, value, key)

        if (len(old_node.values) == old_node.order): #se o no fica cheio, realiza a divisao 
            node1 = Node(old_node.order) #cria um novo nó
            node1.check_leaf = True
            node1.parent = old_node.parent
            mid = int(math.ceil(old_node.order / 2)) - 1 #calcula o valor médio para dividir
            node1.values = old_node.values[mid + 1:]     #organiza as chaves e valores entre o novo e antigo nó*
            node1.keys = old_node.keys[mid + 1:] #*
            node1.nextKey = old_node.nextKey #atualiza o ponteiro**
            old_node.values = old_node.values[:mid + 1] #*
            old_node.keys = old_node.keys[:mid + 1] #*
            old_node.nextKey = node1 #**
            self.insert_in_parent(old_node, node1.values[0], node1) #propaga a divisão

    def search(self, value): #percorre a árvore até encontrar tal valor (retorna o nó)
        current_node = self.root
        while(current_node.check_leaf == False):
            lista_de_valores2 = current_node.values
            for i in range(len(lista_de_valores2)):
                if (value == lista_de_valores2[i]): #valor encontrado, vai direto para o filho
                    current_node = current_node.keys[i + 1]
                    break
                elif (value < lista_de_valores2[i]): #valor é menor, vai para o filho da esquerda
                    current_node = current_node.keys[i]
                    break
                elif (i + 1 == len(current_node.values)): #chegou ao final do nó, vai para o último filho
                    current_node = current_node.keys[i + 1]
                    break
        return current_node 

    def find(self, value, key): #verifica se tal valor-chave existe na arvore (retorna true/false) 
        n = self.search(value) #encontra o nó folha do valor
        for i, item in enumerate(n.values): #encontra o valor 
            if item == value: 
                if key in n.keys[i]:
                    return True #par chave-valor existe
                else:
                    return False #exista valor, mas com outra chave
        return False #valor nao encontrado

    def insert_in_parent(self, n, value, ndash): #gerencia a insercao em um no pai apos uma divisao (nó original, valor separador, novo nó)
        #se o nó dividido for a raiz
        if (self.root == n): 
            rootNode = Node(n.order) #cria nova raiz
            rootNode.values = [value]
            rootNode.keys = [n, ndash]
            self.root = rootNode #atualiza os ponteiros
            n.parent = rootNode
            ndash.parent = rootNode
            return
        #pai tem espaço 
        parentNode = n.parent
        filhos_pai = parentNode.keys #lista de filhos do pai
        for i in range(len(filhos_pai)): #encontra posição do nó "n" no pai 
            if (filhos_pai[i] == n): 
                #insere o valor separador na posição correta
                parentNode.values = parentNode.values[:i] + [value] + parentNode.values[i:]
                parentNode.keys = parentNode.keys[:i + 1] + [ndash] + parentNode.keys[i + 1:]
                #nó pai também fica cheio
                if (len(parentNode.keys) > parentNode.order): 
                    #divide o nó pai também
                    parentdash = Node(parentNode.order)
                    parentdash.parent = parentNode.parent
                    mid = int(math.ceil(parentNode.order / 2)) - 1 #calcula o valor médio para dividir
                    #divide os valores e chaves 
                    parentdash.values = parentNode.values[mid + 1:]
                    parentdash.keys = parentNode.keys[mid + 1:]
                    value_ = parentNode.values[mid] #valor separador que "sobe"
                    #ajusta o nó pai/original
                    if (mid == 0):
                        parentNode.values = parentNode.values[:mid + 1]
                    else:
                        parentNode.values = parentNode.values[:mid]
                    parentNode.keys = parentNode.keys[:mid + 1]
                    #atualiza os ponteiros
                    for j in parentNode.keys:
                        j.parent = parentNode
                    for j in parentdash.keys:
                        j.parent = parentdash
                    self.insert_in_parent(parentNode, value_, parentdash) #propaga a divisão para cima usando recursão

    def delete(self, value, key): #remove uma par valor-chave da arvore 
        node_ = self.search(value) #encontra o nó que contém o valor
        temp = 0
        #procura o valor no nó
        for i, item in enumerate(node_.values):
            if item == value:
                temp = 1 #valor encontrado

                if key in node_.keys[i]: #verifica se a chave informada existe
                    #várias chaves para o mesmo valor
                    if len(node_.keys[i]) > 1:
                        node_.keys[i].pop(node_.keys[i].index(key)) #remove somente a chave
                    #remove chave única da raiz
                    elif node_ == self.root:
                        node_.values.pop(i)
                        node_.keys.pop(i)
                    #remove chave única em nó que nao é raiz
                    else:
                        node_.keys[i].pop(node_.keys[i].index(key))
                        del node_.keys[i]
                        node_.values.pop(node_.values.index(value))
                        self.deleteEntry(node_, value, key) #remove e inicia balanceamento
                else:
                    print("Value not in Key")
                    return
        #valor não encontrado
        if temp == 0:
            print("Value not in Tree")
            return

    def deleteEntry(self, node_, value, key): #rebalanceia a arvore apos uma remocao    
        #se o nó não é uma folha, remove a chave e o valor da lista
        if not node_.check_leaf:
            for i, item in enumerate(node_.keys):
                if item == key:
                    node_.keys.pop(i)
                    break
            for i, item in enumerate(node_.values):
                if item == value:
                    node_.values.pop(i)
                    break
        #se a raiz tem apenas um filho      
        if self.root == node_ and len(node_.keys) == 1: 
            self.root = node_.keys[0] #nova raiz
            node_.keys[0].parent = None #remove o pai
            del node_ #remove o raiz antiga
            return
        #verifica se as propriedades da bplustree estão sendo respeitadas
        elif (len(node_.keys) < int(math.ceil(node_.order / 2)) and node_.check_leaf == False) or (len(node_.values) < int(math.ceil((node_.order - 1) / 2)) and node_.check_leaf == True):

            is_predecessor = 0
            parentNode = node_.parent
            #encontra os vizinhos do nó 
            PrevNode = -1
            NextNode = -1
            PrevK = -1
            PostK = -1
            #encontra a posição do nó no pai
            for i, item in enumerate(parentNode.keys):

                if item == node_:
                    #irmão anterior
                    if i > 0:
                        PrevNode = parentNode.keys[i - 1]
                        PrevK = parentNode.values[i - 1]
                    #irmão posterior
                    if i < len(parentNode.keys) - 1:
                        NextNode = parentNode.keys[i + 1]
                        PostK = parentNode.values[i]
            #escolhe o irmão (preferência a fusão)
            if PrevNode == -1:
                ndash = NextNode
                value_ = PostK
            elif NextNode == -1:
                is_predecessor = 1
                ndash = PrevNode
                value_ = PrevK
            else:
                if len(node_.values) + len(NextNode.values) < node_.order:
                    ndash = NextNode
                    value_ = PostK
                else:
                    is_predecessor = 1
                    ndash = PrevNode
                    value_ = PrevK
            #se os dois cabem em um só, faz a fusão 
            if len(node_.values) + len(ndash.values) < node_.order:
                if is_predecessor == 0:
                    node_, ndash = ndash, node_
                #combina os nós
                ndash.keys += node_.keys
                if not node_.check_leaf:
                    ndash.values.append(value_)
                else:
                    ndash.nextKey = node_.nextKey #liga os ponteiros das folhas
                #combina os nós
                ndash.values += node_.values

                if not ndash.check_leaf:
                    for j in ndash.keys:
                        j.parent = ndash

                self.deleteEntry(node_.parent, value_, node_) #usa recursão para remover o separador do pai
                del node_
            else: #não pode fazer fusão, então redistribui
                if is_predecessor == 1: #redistribuição com antecessor
                    if not node_.check_leaf: #nó interno
                        #move o último filho do antecessor
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm_1 = ndash.values.pop(-1)
                        #adiciona ao inicio do nó atual
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [value_] + node_.values
                        parentNode = node_.parent
                        #atualiza o separador do pai 
                        for i, item in enumerate(parentNode.values): 
                            if item == value_:
                                parentNode.values[i] = ndashkm_1
                                break
                    else: #nó folha
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [ndashkm] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashkm
                                break
                else: #redistribuição com sucessor
                    if not node_.check_leaf:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [value_]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashk0
                                break
                    else:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [ndashk0]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndash.values[0]
                                break
                #atualiza os ponteiros pai-filho
                if not ndash.check_leaf:
                    for j in ndash.keys:
                        j.parent = ndash
                if not node_.check_leaf:
                    for j in node_.keys:
                        j.parent = node_
                if not parentNode.check_leaf:
                    for j in parentNode.keys:
                        j.parent = parentNode


