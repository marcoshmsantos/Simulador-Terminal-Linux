import math

class Node:
    def __init__(self, ordem):
        self.ordem = ordem #define a ordem da árvore
        self.valores = [] #lista com os valores de cada nó
        self.chaves = [] #lista com as chaves que correspondem a cada valor
        self.próxima_chave = None #ponteiro para o proximo nó
        self.pai = None #indica o nó pai, auxilia na divisão de nós
        self.é_folha = False #diz se o nó é folha ou nó interno

    #insere um par valor-chave em uma folha
    def inserção_na_folha(self, folha, valor, chave): 
        if (self.valores): #se o nó ja tem valores.
            lista_de_valores = self.valores
            for i in range(len(lista_de_valores)):
                if (valor == lista_de_valores[i]): #se o valor ja existe, adiciona a chave a lista de chaves 
                    self.chaves[i].append(chave)
                    break
                elif (valor < lista_de_valores[i]): #se o valor é menor, insere na posição correta 
                    self.valores = self.valores[:i] + [valor] + self.valores[i:]
                    self.chaves = self.chaves[:i] + [[chave]] + self.chaves[i:]
                    break
                elif (i + 1 == len(lista_de_valores)): #se o valor é maior, insere no final
                    self.valores.append(valor)
                    self.chaves.append([chave])
                    break
        else: #se o nó esta vazio, inicia a lista com os valores
            self.valores = [valor]
            self.chaves = [[chave]]
 

class BplusTree:
    def __init__(self, ordem):
        self.root = Node(ordem)
        self.root.é_folha = True

    #realiza a inserção
    def inserção(self, valor, chave): 
        valor = str(valor)
        node_antigo = self.busca(valor)
        node_antigo.inserção_na_folha(node_antigo, valor, chave)
        if (len(node_antigo.valores) == node_antigo.ordem): #se o nó fica cheio, realiza a divisão
            node1 = Node(node_antigo.ordem) #cria um novo nó
            node1.é_folha = True
            node1.pai = node_antigo.pai
            mid = int(math.ceil(node_antigo.ordem / 2)) - 1 #calcula o valor médio para dividir
            node1.valores = node_antigo.valores[mid + 1:]     #organiza as chaves e valores entre o novo e antigo nó*
            node1.chaves = node_antigo.chaves[mid + 1:] #*
            node1.próxima_chave = node_antigo.próxima_chave #atualiza o ponteiro**
            node_antigo.valores = node_antigo.valores[:mid + 1] #*
            node_antigo.chaves = node_antigo.chaves[:mid + 1] #*
            node_antigo.próxima_chave = node1 #**
            self.inserção_no_pai(node_antigo, node1.valores[0], node1) #propaga a divisão

    #percorre a árvore até encontrar tal valor (retorna o nó)
    def busca(self, valor): 
        node_atual = self.root
        while(node_atual.é_folha == False):
            lista_de_valores2 = node_atual.valores
            for i in range(len(lista_de_valores2)):
                if (valor == lista_de_valores2[i]): #valor encontrado, vai direto para o filho
                    node_atual = node_atual.chaves[i + 1]
                    break
                elif (valor < lista_de_valores2[i]): #valor é menor, vai para o filho da esquerda
                    node_atual = node_atual.chaves[i]
                    break
                elif (i + 1 == len(node_atual.valores)): #chegou ao final do nó, vai para o último filho
                    node_atual = node_atual.chaves[i + 1]
                    break
        return node_atual 
    
    #verifica se tal chave-valor existe na árvore (retorna true/false)
    def verifica_existência(self, valor, chave):  
        n = self.busca(valor) #encontra o nó folha do valor
        for i, item in enumerate(n.valores): #encontra o valor 
            if item == valor: 
                if chave in n.chaves[i]:
                    return True #par chave-valor existe
                else:
                    return False #exista valor, mas com outra chave
        return False #valor nao encontrado
    
    #gerencia a inserção em um nó pai apos uma divisao (nó original, valor separador, novo nó)
    def inserção_no_pai(self, n, valor, newnode): 
        #se o nó dividido for a raiz
        if (self.root == n): 
            rootNode = Node(n.ordem) #cria nova raiz
            rootNode.valores = [valor]
            rootNode.chaves = [n, newnode]
            self.root = rootNode #atualiza os ponteiros
            n.pai = rootNode
            newnode.pai = rootNode
            return
        #pai tem espaço 
        paiNode = n.pai
        filhos_pai = paiNode.chaves #lista de filhos do pai
        for i in range(len(filhos_pai)): #encontra posição do nó "n" no pai 
            if (filhos_pai[i] == n): 
                #insere o valor separador na posição correta
                paiNode.valores = paiNode.valores[:i] + [valor] + paiNode.valores[i:]
                paiNode.chaves = paiNode.chaves[:i + 1] + [newnode] + paiNode.chaves[i + 1:]
                #nó pai também fica cheio
                if (len(paiNode.chaves) > paiNode.ordem): 
                    #divide o nó pai também
                    paiponteiro = Node(paiNode.ordem)
                    paiponteiro.pai = paiNode.pai
                    mid = int(math.ceil(paiNode.ordem / 2)) - 1 #calcula o valor médio para dividir
                    #divide os valores e chaves 
                    paiponteiro.valores = paiNode.valores[mid + 1:]
                    paiponteiro.chaves = paiNode.chaves[mid + 1:]
                    valor_ = paiNode.valores[mid] #valor separador que "sobe"
                    #ajusta o nó pai/original
                    if (mid == 0):
                        paiNode.valores = paiNode.valores[:mid + 1]
                    else:
                        paiNode.valores = paiNode.valores[:mid]
                    paiNode.chaves = paiNode.chaves[:mid + 1]
                    #atualiza os ponteiros
                    for j in paiNode.chaves:
                        j.pai = paiNode
                    for j in paiponteiro.chaves:
                        j.pai = paiponteiro
                    self.inserção_no_pai(paiNode, valor_, paiponteiro) #propaga a divisão para cima usando recursão

    #busca todos as chaves para determinado valor
    def chaves_valor(self, valor):
        valor = str(valor)
        x = self.busca(valor)
        for i, item in enumerate(x.valores):
            if item == valor:
                return x.chaves[i]
        return []
    
    #coleta todos os pares chave-valor da bplustree
    def todas_entradas(self):
        entradas = []
        def análise_node(node):
            if node.é_folha:
                for i, valor in enumerate(node.valores):
                    for chave in node.chaves[i]:
                        entradas.append((valor, chave))
            else:
                for filho in node.chaves:
                    análise_node(filho)
        análise_node(self.root)
        return entradas
    
    #remove uma par valor-chave da arvore 
    def delete(self, valor, chave): 
        node_ = self.busca(valor) #encontra o nó que contém o valor
        x= 0
        #procura o valor no nó
        for i, item in enumerate(node_.valores):
            if item == valor:
                x= 1 #valor encontrado
                if chave in node_.chaves[i]: #verifica se a chave informada existe
                    #várias chaves para o mesmo valor
                    if len(node_.chaves[i]) > 1:
                        node_.chaves[i].pop(node_.chaves[i].index(chave)) #remove somente a chave
                    #remove chave única da raiz
                    elif node_ == self.root:
                        node_.valores.pop(i)
                        node_.chaves.pop(i)
                    #remove chave única em nó que nao é raiz
                    else:
                        node_.chaves[i].pop(node_.chaves[i].index(chave))
                        del node_.chaves[i]
                        node_.valores.pop(node_.valores.index(valor))
                        self.deleteEntry(node_, valor, chave) #remove e inicia balanceamento
                else:
                    print("valor não é chave")
                    return
        #valor não encontrado
        if x == 0:
            print("valor não está na árvore")
            return
        
    #rebalanceia a arvore após uma remoção
    def deleteEntry(self, node_, valor, chave): 
        #se o nó não é uma folha, remove a chave e o valor da lista
        if not node_.é_folha:
            for i, item in enumerate(node_.chaves):
                if item == chave:
                    node_.chaves.pop(i)
                    break
            for i, item in enumerate(node_.valores):
                if item == valor:
                    node_.valores.pop(i)
                    break
        #se a raiz tem apenas um filho      
        if self.root == node_ and len(node_.chaves) == 1: 
            self.root = node_.chaves[0] #nova raiz
            node_.chaves[0].pai = None #remove o pai
            del node_ #remove o raiz antiga
            return
        #verifica se as propriedades da bplustree estão sendo respeitadas
        elif (len(node_.chaves) < int(math.ceil(node_.ordem / 2)) and node_.é_folha == False) or (len(node_.valores) < int(math.ceil((node_.ordem - 1) / 2)) and node_.é_folha == True):
            antecessor = 0
            paiNode = node_.pai
            #encontra os vizinhos do nó 
            PrevNode = -1
            próximaNode = -1
            PrevK = -1
            PostK = -1
            #encontra a posição do nó no pai
            for i, item in enumerate(paiNode.chaves):
                if item == node_:
                    #irmão anterior
                    if i > 0:
                        PrevNode = paiNode.chaves[i - 1]
                        PrevK = paiNode.valores[i - 1]
                    #irmão posterior
                    if i < len(paiNode.chaves) - 1:
                        próximaNode = paiNode.chaves[i + 1]
                        PostK = paiNode.valores[i]
            #escolhe o irmão (preferência a fusão)
            if PrevNode == -1:
                newnode = próximaNode
                valor_ = PostK
            elif próximaNode == -1:
                antecessor = 1
                newnode = PrevNode
                valor_ = PrevK
            else:
                if len(node_.valores) + len(próximaNode.valores) < node_.ordem:
                    newnode = próximaNode
                    valor_ = PostK
                else:
                    antecessor = 1
                    newnode = PrevNode
                    valor_ = PrevK
            #se os dois cabem em um só, faz a fusão 
            if len(node_.valores) + len(newnode.valores) < node_.ordem:
                if antecessor == 0:
                    node_, newnode = newnode, node_
                #combina os nós
                newnode.chaves += node_.chaves
                if not node_.é_folha:
                    newnode.valores.append(valor_)
                else:
                    newnode.próxima_chave = node_.próxima_chave #liga os ponteiros das folhas
                #combina os nós
                newnode.valores += node_.valores
                if not newnode.é_folha:
                    for j in newnode.chaves:
                        j.pai = newnode
                self.deleteEntry(node_.pai, valor_, node_) #usa recursão para remover o separador do pai
                del node_
            else: #não pode fazer fusão, então redistribui
                if antecessor == 1: #redistribuição com antecessor
                    if not node_.é_folha: #nó interno
                        #move o último filho do antecessor
                        newnodepm = newnode.chaves.pop(-1)
                        newnodekm_1 = newnode.valores.pop(-1)
                        #adiciona ao inicio do nó atual
                        node_.chaves = [newnodepm] + node_.chaves
                        node_.valores = [valor_] + node_.valores
                        paiNode = node_.pai
                        #atualiza o separador do pai 
                        for i, item in enumerate(paiNode.valores): 
                            if item == valor_:
                                paiNode.valores[i] = newnodekm_1
                                break
                    else: #nó folha
                        newnodepm = newnode.chaves.pop(-1)
                        newnodekm = newnode.valores.pop(-1)
                        node_.chaves = [newnodepm] + node_.chaves
                        node_.valores = [newnodekm] + node_.valores
                        paiNode = node_.pai
                        for i, item in enumerate(paiNode.valores):
                            if item == valor_:
                                paiNode.valores[i] = newnodekm
                                break
                else: #redistribuição com sucessor
                    if not node_.é_folha:
                        newnodep0 = newnode.chaves.pop(0)
                        newnodek0 = newnode.valores.pop(0)
                        node_.chaves = node_.chaves + [newnodep0]
                        node_.valores = node_.valores + [valor_]
                        paiNode = node_.pai
                        for i, item in enumerate(paiNode.valores):
                            if item == valor_:
                                paiNode.valores[i] = newnodek0
                                break
                    else:
                        newnodep0 = newnode.chaves.pop(0)
                        newnodek0 = newnode.valores.pop(0)
                        node_.chaves = node_.chaves + [newnodep0]
                        node_.valores = node_.valores + [newnodek0]
                        paiNode = node_.pai
                        for i, item in enumerate(paiNode.valores):
                            if item == valor_:
                                paiNode.valores[i] = newnode.valores[0]
                                break
                #atualiza os ponteiros pai-filho
                if not newnode.é_folha:
                    for j in newnode.chaves:
                        j.pai = newnode
                if not node_.é_folha:
                    for j in node_.chaves:
                        j.pai = node_
                if not paiNode.é_folha:
                    for j in paiNode.chaves:
                        j.pai = paiNode


#representação dos elementos do sistema
class FileSystemEntry:

    def __init__(self, name, é_diretório=False, conteúdo="", pai=None):
        self.name = name #nome do arquivo
        self.é_diretório = é_diretório #define se é diretório 
        self.conteúdo = conteúdo #texto usado para arquivos
        self.pai= pai #aponta para o diretório pai
        if é_diretório:
            self.filhos = BplusTree(5) #cria uma árvore para o diretório
        else:
            self.filhos = None

    #define o pai do filho e insere na bplustree
    def add_filho(self, filho):
        filho.pai= self
        self.filhos.inserção(filho.name, filho)

    #remove o valor
    def remove_filho(self, name):
        filho_entries = self.filhos.chaves_valor(name)
        if filho_entries:
            filho = filho_entries[0]
            self.filhos.delete(name, filho)
            filho.pai= None
            return True
        return False
    
    #busca por nome na bplustree
    def busca_filho(self, name):
        if not self.é_diretório:
            return None
        filho_entries = self.filhos.chaves_valor(name)
        return filho_entries[0] if filho_entries else None
    
    #coleta todos os filhos da árvore
    def lista_filhos(self):
        if not self.é_diretório:
            return []
        filhos = []
        for name, filho in self.filhos.todas_entradas():
            filhos.append(filho)
        filhos.sort(key=lambda x: x.name)
        return filhos
    
    #obtem o path até o pai 
    def path(self):
        if self.pai is None:
            return "/" if self.name == "/" else self.name
        pai_path = self.pai.path()
        if pai_path == "/":
            return "/" + self.name
        else:
            return pai_path + "/" + self.name


#gerencia o sistema e interpreta comando dos usuários
class LinuxTerminalSimulator:

    def __init__(self):
        self.root = FileSystemEntry("/", é_diretório=True) #diretório raiz
        self.dir_atual = self.root #diretório atual
        #nomes de usuário e entidade
        self.username = "user"
        self.hostname = "linux-sim"
        #cria estruturas básicas necessárias
        dir_home = FileSystemEntry("home", é_diretório=True)
        self.root.add_filho(dir_home)
        dir_user = FileSystemEntry(self.username, é_diretório=True)
        dir_home.add_filho(dir_user)
        self.dir_atual = dir_user

    #obtém o path completo do diretório atual
    def prompt(self):
        path_atual = self.dir_atual.path()
        return f"{self.username}@{self.hostname}:{path_atual}$ "
    
    def resolve_path(self, path):
        #retorna diretório atual
        if not path or path == ".":
            return self.dir_atual
        #retorna diretório pai (ou atual se for a raiz)
        if path == "..":
            return self.dir_atual.pai if self.dir_atual.pai else self.dir_atual
        #divide o path em partes e trabalha com as informações
        if path.startswith("/"):
            atual = self.root
            if path == "/":
                return atual
            partes = [p for p in path.split("/") if p]
        else:
            atual = self.dir_atual
            partes = path.split("/")
        for parte in partes:
            if parte == ".":
                continue
            elif parte == "..":
                atual = atual.pai if atual.pai else atual
            else:
                if not atual.é_diretório:
                    return None
                filho = atual.busca_filho(parte)
                if filho is None:
                    return None
                atual = filho
        return atual
    
    #lista os diretórios e arquivos no diretório atual
    def cmd_ls(self, args):
        #sem argumentos, diretório atual
        if not args:
            alvo = self.dir_atual
        #com argumento, lista arquivos e diretórios
        else:
            alvo = self.resolve_path(args[0])
            if alvo is None:
                return f"ls: '{args[0]}' não pode ser acessado: Arquivo ou Diretório inexistente" # mensagem de erro
        #se for arquivo retorna somente o arquivo
        if not alvo.é_diretório:
            return alvo.name
        #se for diretório vazio retorna "", diretório com conteúdo retorna os arquivos 
        filhos = alvo.lista_filhos()
        if not filhos:
            return ""
        return "\n".join(filho.name for filho in filhos)
    
    #navega pelos diretórios
    def cmd_cd(self, args):
        #sem argumentos, vai para diretório inicial
        if not args:
            home_path = f"/home/{self.username}"
            alvo = self.resolve_path(home_path)
        #com argumento, vai para diretório especificado
        else:
            alvo = self.resolve_path(args[0])
        #mensagens de erro, path inválido e diretório inexistente 
        if alvo is None:
            path = args[0] if args else f"/home/{self.username}"
            return f"cd: {path}: Arquivo ou Diretório inexistente"
        if not alvo.é_diretório:
            return f"cd: {args[0] if args else 'alvo'}: Não é um Diretório"
        #atualiza o diretório atual
        self.dir_atual = alvo
        return ""
    
    #cria diretórios
    def cmd_mkdir(self, args):
        #exige argumento 
        if not args:
            return "mkdir: erro ao operar"
        #cria os diretórios e trata entradas inválidas
        for dir_name in args:
            if "/" in dir_name:
                return f"mkdir: comando não suportado"
            if self.dir_atual.busca_filho(dir_name):
                return f"mkdir: '{dir_name}' diretório nao pode ser criado: Arquivo existente"
            new_dir = FileSystemEntry(dir_name, é_diretório=True)
            self.dir_atual.add_filho(new_dir)
        return ""
    
    #cria arquivos
    def cmd_touch(self, args):
        #exige argumento
        if not args:
            return "touch: erro ao operar"
        #cria novos arquivos e trata entradas inválidas
        for nome_arquivo in args:
            if "/" in nome_arquivo:
                return f"touch: comando não suportado"
            arquivo_existente = self.dir_atual.busca_filho(nome_arquivo)
            if not arquivo_existente:
                novo_arquivo = FileSystemEntry(nome_arquivo, conteúdo="")
                self.dir_atual.add_filho(novo_arquivo)
        return ""
    
    #remove arquivos e diretórios vazios
    def cmd_rm(self, args):
        #exige argumento
        if not args:
            return "rm: erro ao operar"
        #remove diretórios vazios e arquivos, trata entradas inválidas
        for nome_arquivo in args:
            if "/" in nome_arquivo:
                return f"rm: comando não suportado"
            alvo = self.dir_atual.busca_filho(nome_arquivo)
            if not alvo:
                return f"rm: '{nome_arquivo}' não pode ser removido: Arquivo ou Diretório inexistente"
            if alvo.é_diretório and alvo.lista_filhos():
                return f"rm: '{nome_arquivo}' não pode ser removido: diretório não vazio"
            self.dir_atual.remove_filho(nome_arquivo)
        return ""
    
    #executa os comandos
    def execute_comandos(self, linha_comandos):
        if not linha_comandos.strip():
            return ""
        #torna as entradas padrão
        partes = linha_comandos.strip().split()
        cmd = partes[0].lower()
        args = partes[1:]
        #mapeia comandos e funções
        comandos = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "mkdir": self.cmd_mkdir,
            "touch": self.cmd_touch,
            "rm": self.cmd_rm,
        }
        #chama os comandos e trata entradas inválidas
        if cmd in comandos:
            try:
                return comandos[cmd](args)
            except Exception as e:
                return f"Erro ao executar {cmd}: {str(e)}"
        else:
            return f"{cmd}: comando não encontrado"
        
    #loop principal, exibe prompt e aguarda entrada
    def run(self):
        while True:
            comandos = input(self.prompt())    
            resultado = self.execute_comandos(comandos)
            if resultado:
                print(resultado)

if __name__ == "__main__":
    terminal = LinuxTerminalSimulator()
    terminal.run()