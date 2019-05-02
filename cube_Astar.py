"""
Solução para o problema do deslocamento de um ponto a outro em um cubo com
algumas coordenadas, deste espaço, bloqueadas.
Este programa propõe uma solução para o problema utilizando um algorítmo de
busca A-estrela.

Aluno: Eduardo Machado de Lima
Matrícula: 201620605
"""

"""
Bibliotecas utilizadas:
    random: Para criar os pontos bloqueados do cubo e os de partida e chegada
    aleatíriamente
    time: Para obter os dados de tempo de execução
    pickle: Para guardar os dados de tempo e os bloqueios do cubo
"""
import random
import time
import pickle

"""
Parâmetros do Problema:
    tam (int): Tamanho do cubo
    block (float): Parcela do cubo que será bloqueada
    OP (List): Lista com os possíveis operadores para a solução
"""
tam = 10
block = 0.4
OP = [[1,0,0],      # >
      [-1,0,0],     # <
      [0,1,0],      # ^
      [0,-1,0],     # v
      [0,0,1],      # x
      [0,0,-1]]     # .

def set_DATA():
    """
    Função que:
        Se os dados de tempo já existirem, importa-os para o vetor DATA
        
        Se os dados ainda não existirem, cria um vetor vazio para os dados serem
        adicionados
    
    DATA (list): Vetor com os valores de tempo médio para cada distância e a 
    quantidade de ocorrências obtidos nos testes
    Formato: índice = distância [[tempo médio, ocorrências],...]
    """
    global DATA
    try:
        with open('times_data', 'rb') as fp:
            DATA = pickle.load(fp)
            print("Dados de tempo importados")
            fp.close()
    except IOError:
        print("Iniciando novos dados de tempo...")
        DATA = []


def DATA_write(d,t):
    """
    Função para adicionar um novo valor de tempo obtido aos dados de tempos médios
    
    Argumentos:
        d (int): Distância percorrida para chegar ao objetivo
        t (float): Tempo para encontrar o objetivo
    """
    global DATA
    while len(DATA) < d+1:
        DATA.append([0,0])
    DATA[d][0] = (DATA[d][0]*DATA[d][1] + t)/(DATA[d][1]+1.)
    DATA[d][1] = DATA[d][1] + 1

def rand_xyz():
    """
    Função para gerar um vetor com três números inteiros randômicos que serão 
    utilizados como coordenadas no espaço
    
    Retorno:
        (list): vetor com três números inteiros randômicos que serão utilizados
        como coordenadas no espaço
        Formato: [x,y,z]
    """
    return [random.randint(0,tam-1),    #x
            random.randint(0,tam-1),    #y
            random.randint(0,tam-1)]    #z


def set_BLOCKED():    
    """
    Função que:
        Se os dados de bloqueio já existirem, importa-os para o vetor BLOCKED
        
        Se os dados ainda não existirem, cria um vetor com as coordenadas
        bloqueadas no espaço
        
    BLOCKED (list): Vetor com coordenadas bloqueadas no espaço
    Formato: [[x,y,z],...]
    """
    global BLOCKED
    try:
        with open('blocked_cube', 'rb') as fp:
            BLOCKED = pickle.load(fp)
            print("Dados bloqueio importados")
            fp.close()
    except IOError:
        print("Bloqueando cubo...")
        BLOCKED = []
        while len(BLOCKED) < int(tam**3*block):        
            xyz = rand_xyz()
            if xyz not in BLOCKED:
                BLOCKED.append(xyz)
        with open('blocked_cube', 'wb') as fp:
            print("Salvando bloqueios do cubo...")
            pickle.dump(BLOCKED, fp)
            fp.close()

def set_GAME():    
    """
    Função que escolhe aleatóriamente um ponto de partida e um de chegada dentro
    do cubo, cuidando para que não sejam iguais e não sejam pontos bloqueados
    
    GAME (list): Vetor com as coordenadas da partida e as da chegada
    Formato: [[x_Partida, y_Partida, z_Partida][x_Chegada, y_Chegada, z_Chegada]]
    """
    global GAME
    GAME = []
    while len(GAME) < 2:        
        xyz = rand_xyz()
        if xyz not in BLOCKED and xyz not in GAME:
            GAME.append(xyz)

class Node:
    """
    Classe Node:
        Define atributos e métodos para descrever um nó no caminho e gerar seus
        sucessores
    
    Parâmetros de inicialização:
        x, y, z (int): Valores das coordenadas do nó a ser gerado
    
    Atributos: 
        xyz (list): Coordenadas do nó no espaço do cubo. Formato: [x,y,z]
        valido (bool): Indica se o nó é válido de acordo com o problema proposto
        is_Objetivo (bool): Indica se o nó é o objetivo a ser atingido pela solução do problema proposto
        nxt (List): Lista que guardará os próximos nós gerados pelo nó
        way (int): Quantidade de nós percorridos para chegar no nó
        dist (float): Distância em linha reta entre o nó e o objetivo
    """
    def __init__(self,x,y,z):
        self.xyz = [x,y,z]
        
        self.valido = self.teste_Node()
        self.is_Objetivo = self.teste_Objetivo()
        self.nxt = []
        self.way = 0
        self.dist = self.calc_Dist()
    
    def teste_Node(self):
        """
        Método para informar se o nó é válido de acordo com o problema proposto
        
        Retornos:
            False:
                Se as coordenadas do nó extrapolarem espaço do cubo
                Se o nó for um ponto do cubo bloqueado
            True:
                Se o nó estiver de acordo com todas as regras do problema proposto
        """
        for c in self.xyz:
            if c < 0 or c >= tam: #saiu do cubo
                return False
        
        if self.xyz in BLOCKED: #caminho bloqueado
            return False
        else:
            return True
    
    def teste_Objetivo(self):
        """
        Método para informar se o estado é o objetivo a ser atingido pela solução do problema proposto
        
        Retornos:
            True: Se as coordenadas do nó forem as do objetivo
            False: Se as coordenadas do nó não forem as do objetivo
        """
        if self.xyz == GAME[1]:
            return True
        else:
            return False
    
    def next_Node(self):
        """
        Método que adiciona os próximos nós possivies válidos, geradas pelos 
        operadores do problema, à lista nxt
        """
        men_custo = tam**3 - (tam**3)*block
        for op in OP:
            new = Node(self.xyz[0]+op[0],self.xyz[1]+op[1],self.xyz[2]+op[2])
            
            if new.valido:
                new.way = self.way + 1
                if new.calc_Custo() < men_custo:
                    self.nxt = []
                    self.nxt.append(new)
                    men_custo = new.calc_Custo()
                elif new.calc_Custo() == men_custo:
                    self.nxt.append(new)
                    
    
    def calc_Dist(self):
        """
        Método calcula a distância em linha reta do nó até o objetivo
        
        Retorno:
            (float): Distância em linha reta do nó até o objetivo
        """
        s = 0
        for i in range(3):
            s = s + float((GAME[1][i]-self.xyz[i])**2)
        
        return float(s**(1/2))
    
    def calc_Custo(self):
        """
        Método que calcula o custo do nó
        
        Retorno:
            (float): Custo do nó
        """
        return self.way + self.dist
    
    def __str__(self):
        """
        Método para definir uma representação da classe como uma string (str)
        """
        return str(self.xyz)
       

def play_Game():
    """
    Cria um nó inicial, adiciona-o à fila de nós e inicia a varredura 
    a procura do nó objetivo
    """    
    set_GAME()
    NODES = []
    
    start_Node = Node(GAME[0][0],GAME[0][1],GAME[0][2])
    NODES.append(start_Node)

    t0 = time.clock()
    while True:
        if len(NODES) > 0:
            if NODES[0].is_Objetivo:#Se o nó sendo testado for o objetivo do problema proposto
                """
                Termina a contagem do tempo e salva os dados do jogo em DATA e
                no arquivo times_data
                """
                tf = time.clock()
                if(tf-t0 != 0):
                    print("Objetivo encontrado:\nDistância:",NODES[0].way,"Tempo:",tf-t0)
                    DATA_write(NODES[0].way,tf-t0)                    
                    with open('times_data', 'wb') as fp:
                        pickle.dump(DATA, fp)
                        fp.close()

                return NODES[0].way
                break
                
                return NODES[0].way
            else:
                NODES[0].next_Node()
                
            for n in NODES[0].nxt: 
                NODES.append(n)
            
            NODES.remove(NODES[0])
            
        else:
            break
        if(time.clock() - t0 > 32):
            break

def main():
    set_DATA()
    set_BLOCKED()
    while True:
        play_Game()
       
if __name__ == "__main__":
    main()

    
