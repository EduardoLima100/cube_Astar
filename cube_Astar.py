import random
import time
import pickle

tam = 10
block = 0.4
OP = [[1,0,0],      # >
      [-1,0,0],     # <
      [0,1,0],      # ^
      [0,-1,0],     # v
      [0,0,1],      # x
      [0,0,-1]]     # .

global DATA
try:
    with open('times_data', 'rb') as fp:
        DATA = pickle.load(fp)
        fp.close()
except IOError:
    print("Saindo do início")
    DATA = []

def DATA_write(d,t):
    global DATA
    while len(DATA) < d+1:
        DATA.append([0,0])
    DATA[d][0] = (DATA[d][0]*DATA[d][1] + t)/(DATA[d][1]+1.)
    DATA[d][1] = DATA[d][1] + 1

def rand_xyz():
    return [random.randint(0,tam-1),
            random.randint(0,tam-1),
            random.randint(0,tam-1)]


def set_BLOCKED():    
    global BLOCKED
    try:
        with open('blocked_cube', 'rb') as fp:
            BLOCKED = pickle.load(fp)
    except IOError:
        print("Bloqueando cubo")
        BLOCKED = []
        while len(BLOCKED) < int(tam**3*block):        
            xyz = rand_xyz()
            if xyz not in BLOCKED:
                BLOCKED.append(xyz)
        with open('blocked_cube', 'wb') as fp:
            pickle.dump(BLOCKED, fp)
            fp.close()
    
    
    #print("\n\nBLOCKED = ",BLOCKED)

def set_GAME():    
    global GAME
    GAME = []
    while len(GAME) < 2:        
        xyz = rand_xyz()
        if xyz not in BLOCKED and xyz not in GAME:
            GAME.append(xyz)
    
    #print(time.strftime("\n[%H:%M:%S]"))
    #print("Início: ", GAME[0], "\nObjetivo: ", GAME[1])

class Node:
    def __init__(self,x,y,z):
        self.xyz = [x,y,z]
        
        self.valido = self.teste_Node()
        self.is_Objetivo = self.teste_Objetivo()
        self.nxt = []
        self.way = 0
        self.dist = self.calc_Dist()
    
    def teste_Node(self):
        for c in self.xyz:
            if c < 0 or c >= tam: #saiu do cubo
                return False
        
        if self.xyz in BLOCKED: #caminho bloqueado
            return False
        else:
            return True
    
    def teste_Objetivo(self):
        if self.xyz == GAME[1]:
            return True
        else:
            return False
    
    def next_Node(self):
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
        s = 0
        for i in range(3):
            s = s + float((GAME[1][i]-self.xyz[i])**2)
        
        return float(s**(1/2))
    
    def calc_Custo(self):
        return self.way + self.dist
    
    def __str__(self):
        return str(self.xyz)
       

def main():
    NODES = []
    
    set_BLOCKED()
    
    soma = 0
    while(soma**(1/2)<29):
        set_GAME()
        for i in range(3):
            soma = soma + (GAME[1][i]-GAME[0][i])**2
    
    start_Node = Node(GAME[0][0],GAME[0][1],GAME[0][2])
    #print("Distância em linha reta:", start_Node.calc_Dist())
    
    NODES.append(start_Node)

    t0 = time.clock()
    while True:
        if(time.clock() - t0 > 5):
            return 0
        if len(NODES) > 0:
            #print(NODES[0])
            if NODES[0].is_Objetivo:
                tf = time.clock()
                #print(time.strftime("\n[%H:%M:%S]"))
                #print("Objetivo encontrado!")
                
                #print(NODES[0])
                #print("Distância percorrida:", NODES[0].way)
                if(tf-t0 != 0):
                    DATA_write(NODES[0].way,tf-t0)
                    print("\n", NODES[0].way, end=' ')
                    print(DATA[NODES[0].way],len(DATA)-1,tf-t0)
                    
                    with open('times_data', 'wb') as fp:
                        pickle.dump(DATA, fp)
                        fp.close()
                else:
                   print(".", end=' ')
                return NODES[0].way
                break
                
                return NODES[0].way
            else:
                NODES[0].next_Node()
                
            for n in NODES[0].nxt: 
                NODES.append(n)
            
            NODES.remove(NODES[0])
            
        else:
            #print(time.strftime("\n[%H:%M:%S]"))
            #print("Todas as possibilidades foram testadas\nSolução não existe")
            print('-', end=' ')
            break
        
if __name__ == "__main__":
    global t0;
    print(time.strftime("\n[%H:%M:%S]"))
    global maior_tempo
    maior_tempo = 0
    while True:
        v = main()
        if v == 0:
            print("/", end='')
#        elif(v!=0 and v!=None):
#            tf = time.time()
#            #print("Tempo gasto:", tf-t0)
#            if tf-t0 > maior_tempo:
#                maior_tempo = tf-t0
#                print("\nMaior tempo:",maior_tempo, "Distancia:",v)
    
