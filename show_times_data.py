"""
Este programa mostra os dados obtidos pelo cube_Astar.py

Aluno: Eduardo Machado de Lima
Matrícula: 201620605
"""

"""
Bibliotecas utilizadas:
    pickle: Para guardar os dados de tempo e os bloqueios do cubo
    matplotlib.pyplot: Para plotar o gráfico dos dados
"""
import pickle
import matplotlib.pyplot as plt

def print_DATA(DATA):
    """
    Função para imprimir os dados na tela
    """
    print("Distância:","\tTempo médio:","\t\t\tOcorrências:")
    for i in range(len(DATA)):
        print(DATA[i][0],"\t|\t","%.20f"%DATA[i][1],"\t|\t",DATA[i][2])


def main():
    """
    Função main trata os dados para mostrar, pegando apenas os que tiverem
    mais que 50 ocorrências e os mostra impressos e em um grafico
    """
    try:
        with open('times_data', 'rb') as fp:
            DATA = pickle.load(fp)
            fp.close()
    except IOError:
        print("Não há dados")
        
    if(len(DATA)>0):
        DT = []
        for i in range(len(DATA)):
            DT.append([i]+DATA[i])
        
        i = 0
        while i < len(DT):
            if DT[i][2] < 50:
                DT.remove(DT[i])
            else:
                i=i+1
        
        print_DATA(DT)
        
        X = []
        for x in DT:
            X.append(x[0])
        Y = []
        for y in DT:
            Y.append(y[1])
        
        
        
        plt.rcParams['figure.figsize'] = (7,7)
        plt.plot(X,Y)
        plt.grid()
        plt.show()

if __name__ == "__main__":
    main()

        
