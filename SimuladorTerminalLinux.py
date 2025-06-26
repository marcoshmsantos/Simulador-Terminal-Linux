import math
from BPlustree import BplusTree

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
