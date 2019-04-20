import random

TAM = 4
BLOCK = 0.4
OP = [[1,0,0],      # >
      [-1,0,0],     # <
      [0,1,0],      # ^
      [0,-1,0],     # v
      [0,0,1],      # x
      [0,0,-1]]     # .

NODES = []

def rand_xyz():
    return [random.randint(0,TAM-1),
            random.randint(0,TAM-1),
            random.randint(0,TAM-1)]

BLOCKED = []
while len(BLOCKED) < int(TAM**3*BLOCK):        
    xyz = rand_xyz()
    if xyz not in BLOCKED:
        BLOCKED.append(xyz)
print("BLOCKED = ",BLOCKED)

GAME = []
while len(GAME) < 2:        
    xyz = rand_xyz()
    if xyz not in BLOCKED and xyz not in GAME:
        GAME.append(xyz)
print("\nInício: ", GAME[0], "\nObjetivo: ", GAME[1])
    

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
            if c < 0 or c >= TAM: #saiu do cubo
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
        men_custo = TAM**3
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
            s = (GAME[1][i]-self.xyz[i])**2
        #print("Dist: ",s)
        return s**(1/2)
    
    def calc_Custo(self):
        return self.way + self.dist
    
    def __str__(self):
        return str(self.xyz)
        
CAMINHOX = []
CAMINHOY = []
CAMINHOZ = []
def main():
    start_Node = Node(GAME[0][0],GAME[0][1],GAME[0][2])
    NODES.append(start_Node)

    loop = True
    while loop:
        if len(NODES) > 0:
            #print(NODES[0])
            if NODES[0].is_Objetivo:
                print("Objetivo encontrado!")
                print(NODES[0])
                loop = False
            else:
                NODES[0].next_Node()
                
            for n in NODES[0].nxt: 
                NODES.append(n)
            
            NODES.remove(NODES[0])
        else:
            print("Todas as possibilidades foram testadas\nSolução não existe")
            loop = False

if __name__ == "__main__":
    main()
    